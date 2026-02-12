from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import io
import csv
import ssl
import ipaddress
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
import tempfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-key'

db = SQLAlchemy(app)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    records = db.relationship('ExpenseRecord', backref='vehicle', lazy=True)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    member_type = db.Column(db.String(32), default='Member')
    records = db.relationship('ExpenseRecord', backref='member', lazy=True)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), unique=True, nullable=False)
    value = db.Column(db.String(1024), nullable=True)


class ExpenseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)

    single_way_km = db.Column(db.Float, default=0.0)
    double_way_km = db.Column(db.Float, default=0.0)
    single_total_cost = db.Column(db.Float, default=0.0)
    double_total_cost = db.Column(db.Float, default=0.0)

    tds_1_percent = db.Column(db.Float, default=0.0)
    maintenance = db.Column(db.Float, default=0.0)
    driver_salary = db.Column(db.Float, default=0.0)
    vehicle_maintenance = db.Column(db.Float, default=0.0)
    cng_gas = db.Column(db.Float, default=0.0)
    petrol = db.Column(db.Float, default=0.0)
    supervisor_commission = db.Column(db.Float, default=0.0)

    company_credit = db.Column(db.Float, default=0.0)
    total_deduction = db.Column(db.Float, default=0.0)
    total_profit_after_tax = db.Column(db.Float, default=0.0)


@app.route('/')
def index():
    vehicles = Vehicle.query.all()
    records = ExpenseRecord.query.order_by(ExpenseRecord.id.desc()).all()
    return render_template('index.html', vehicles=vehicles, records=records)


@app.route('/settings')
def manage_fleet():
    vehicles = Vehicle.query.all()
    members = Member.query.all()
    return render_template('settings.html', vehicles=vehicles, members=members)


@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    name = request.form.get('vehicle_name', '').strip()
    if name:
        vehicle = Vehicle(name=name)
        db.session.add(vehicle)
        db.session.commit()
        flash(f'Car "{name}" added successfully!', 'success')
    return redirect(url_for('settings'))


@app.route('/delete_vehicle', methods=['POST'])
def delete_vehicle():
    vehicle_id = request.form.get('vehicle_id')
    if vehicle_id:
        vehicle = Vehicle.query.get(int(vehicle_id))
        if vehicle:
            # Delete associated records first
            ExpenseRecord.query.filter_by(vehicle_id=vehicle.id).delete()
            db.session.delete(vehicle)
            db.session.commit()
            flash('Car deleted successfully!', 'success')
    return redirect(url_for('settings'))


@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form.get('member_name', '').strip()
    member_type = request.form.get('member_type', 'Member')
    if name:
        member = Member(name=name, member_type=member_type)
        db.session.add(member)
        db.session.commit()
        flash(f'{name} added successfully!', 'success')
    return redirect(url_for('settings'))


@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = request.form.get('member_id')
    if member_id:
        member = Member.query.get(int(member_id))
        if member:
            # Delete associated records first
            ExpenseRecord.query.filter_by(member_id=member.id).delete()
            db.session.delete(member)
            db.session.commit()
            flash('Member deleted successfully!', 'success')
    return redirect(url_for('settings'))


@app.route('/add', methods=['GET', 'POST'])
def add_record():
    vehicles = Vehicle.query.all()
    members = Member.query.all()
    if request.method == 'POST':
        data = request.form
        def f(name):
            try:
                return float(data.get(name) or 0)
            except ValueError:
                return 0.0

        record = ExpenseRecord(
            month=data.get('month') or '',
            vehicle_id=int(data.get('vehicle_id')),
            member_id=int(data.get('member_id')) if data.get('member_id') else None,
            single_way_km=f('single_way_km'),
            double_way_km=f('double_way_km'),
            single_total_cost=f('single_total_cost'),
            double_total_cost=f('double_total_cost'),
            tds_1_percent=f('tds_1_percent'),
            maintenance=f('maintenance'),
            driver_salary=f('driver_salary'),
            vehicle_maintenance=f('vehicle_maintenance'),
            cng_gas=f('cng_gas'),
            petrol=f('petrol'),
            supervisor_commission=f('supervisor_commission'),
            company_credit=f('company_credit')
        )

        record.total_deduction = (
            record.tds_1_percent + record.maintenance + record.driver_salary
            + record.vehicle_maintenance + record.cng_gas + record.petrol
            + record.supervisor_commission
        )
        record.total_profit_after_tax = record.company_credit - record.total_deduction

        db.session.add(record)
        db.session.commit()
        flash('Record added', 'success')
        return redirect(url_for('index'))

    return render_template('add_record.html', vehicles=vehicles, members=members)


@app.route('/initdb')
def initdb():
    db.create_all()
    # Add member_type column if it doesn't exist
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE member ADD COLUMN member_type VARCHAR(32) DEFAULT "Member"'))
        db.session.commit()
    except Exception:
        pass  # Column already exists
    
    if Vehicle.query.count() == 0:
        vnames = ['Car A', 'Car B', 'Car C']
        for n in vnames:
            db.session.add(Vehicle(name=n))
    if Member.query.count() == 0:
        mnames = ['Owner', 'Driver1', 'Driver2', 'Supervisor']
        for n in mnames:
            member = Member(name=n, member_type='Driver' if 'Driver' in n else 'Member')
            db.session.add(member)
    db.session.commit()
    return 'DB initialized with sample vehicles and members. <a href="/">Go to Dashboard</a> | <a href="/settings">Manage Cars & Drivers</a>'


@app.route('/export_csv')
def export_csv():
    vehicle_id = request.args.get('vehicle_id')
    month = request.args.get('month')
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')
    q = ExpenseRecord.query
    if vehicle_id:
        try:
            q = q.filter(ExpenseRecord.vehicle_id == int(vehicle_id))
        except Exception:
            pass
    if month:
        q = q.filter(ExpenseRecord.month.ilike(f"%{month}%"))
    # If start/end provided (format YYYY-MM), do lexicographic compare
    if start_month:
        q = q.filter(ExpenseRecord.month >= start_month)
    if end_month:
        q = q.filter(ExpenseRecord.month <= end_month)
    records = q.order_by(ExpenseRecord.id).all()
    si = io.StringIO()
    writer = csv.writer(si)
    header = [
        'id','month','vehicle','member','single_way_km','double_way_km',
        'single_total_cost','double_total_cost','tds_1_percent','maintenance',
        'driver_salary','vehicle_maintenance','cng_gas','petrol','supervisor_commission',
        'company_credit','total_deduction','total_profit_after_tax'
    ]
    writer.writerow(header)
    for r in records:
        writer.writerow([
            r.id, r.month, r.vehicle.name if r.vehicle else '', r.member.name if r.member else '',
            r.single_way_km, r.double_way_km, r.single_total_cost, r.double_total_cost,
            r.tds_1_percent, r.maintenance, r.driver_salary, r.vehicle_maintenance,
            r.cng_gas, r.petrol, r.supervisor_commission, r.company_credit,
            r.total_deduction, r.total_profit_after_tax
        ])
    mem = BytesIO()
    mem.write(si.getvalue().encode('utf-8'))
    mem.seek(0)
    filename = f"fleet_records_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(mem, mimetype='text/csv', download_name=filename, as_attachment=True)


@app.route('/import_csv', methods=['GET', 'POST'])
def import_csv():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            flash('No file uploaded', 'danger')
            return redirect(url_for('import_csv'))
        stream = io.StringIO(f.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        created = 0
        for row in reader:
            # find or create vehicle
            vname = (row.get('vehicle') or '').strip()
            if vname:
                vehicle = Vehicle.query.filter_by(name=vname).first()
                if not vehicle:
                    vehicle = Vehicle(name=vname)
                    db.session.add(vehicle)
                    db.session.flush()
            else:
                continue

            mname = (row.get('member') or '').strip()
            member = None
            if mname:
                member = Member.query.filter_by(name=mname).first()
                if not member:
                    member = Member(name=mname)
                    db.session.add(member)
                    db.session.flush()

            def fval(k):
                try:
                    return float(row.get(k) or 0)
                except Exception:
                    return 0.0

            rec = ExpenseRecord(
                month=row.get('month') or '',
                vehicle_id=vehicle.id,
                member_id=member.id if member else None,
                single_way_km=fval('single_way_km'),
                double_way_km=fval('double_way_km'),
                single_total_cost=fval('single_total_cost'),
                double_total_cost=fval('double_total_cost'),
                tds_1_percent=fval('tds_1_percent'),
                maintenance=fval('maintenance'),
                driver_salary=fval('driver_salary'),
                vehicle_maintenance=fval('vehicle_maintenance'),
                cng_gas=fval('cng_gas'),
                petrol=fval('petrol'),
                supervisor_commission=fval('supervisor_commission'),
                company_credit=fval('company_credit')
            )
            rec.total_deduction = (
                rec.tds_1_percent + rec.maintenance + rec.driver_salary
                + rec.vehicle_maintenance + rec.cng_gas + rec.petrol
                + rec.supervisor_commission
            )
            rec.total_profit_after_tax = rec.company_credit - rec.total_deduction
            db.session.add(rec)
            created += 1
        db.session.commit()
        flash(f'Imported {created} records', 'success')
        return redirect(url_for('index'))

    return render_template('import.html')


@app.route('/report_pdf')
def report_pdf():
    # allow optional filters
    vehicle_id = request.args.get('vehicle_id')
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')
    q = ExpenseRecord.query
    if vehicle_id:
        try:
            q = q.filter(ExpenseRecord.vehicle_id == int(vehicle_id))
        except Exception:
            pass
    if start_month:
        q = q.filter(ExpenseRecord.month >= start_month)
    if end_month:
        q = q.filter(ExpenseRecord.month <= end_month)
    records = q.order_by(ExpenseRecord.id).all()
    mem = BytesIO()
    c = canvas.Canvas(mem, pagesize=letter)
    width, height = letter
    x = 40
    y = height - 40
    c.setFont('Helvetica-Bold', 14)
    c.drawString(x, y, 'Fleet Expense Report')
    c.setFont('Helvetica', 9)
    y -= 20
    header = ['ID','Month','Vehicle','Member','Credit','Profit']
    c.drawString(x, y, ' | '.join(header))
    y -= 12
    for r in records:
        line = f"{r.id} | {r.month} | {r.vehicle.name if r.vehicle else ''} | {r.member.name if r.member else ''} | {r.company_credit:.2f} | {r.total_profit_after_tax:.2f}"
        c.drawString(x, y, line)
        y -= 12
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    mem.seek(0)
    filename = f"fleet_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(mem, mimetype='application/pdf', download_name=filename, as_attachment=True)


@app.route('/report_pdf_vehicle')
def report_pdf_vehicle():
    # per-vehicle PDF, optional date range
    vehicle_id = request.args.get('vehicle_id')
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')
    if not vehicle_id:
        flash('vehicle_id is required', 'danger')
        return redirect(url_for('index'))
    try:
        vid = int(vehicle_id)
    except Exception:
        flash('Invalid vehicle id', 'danger')
        return redirect(url_for('index'))
    vehicle = Vehicle.query.get(vid)
    if not vehicle:
        flash('Vehicle not found', 'danger')
        return redirect(url_for('index'))

    q = ExpenseRecord.query.filter(ExpenseRecord.vehicle_id == vid)
    if start_month:
        q = q.filter(ExpenseRecord.month >= start_month)
    if end_month:
        q = q.filter(ExpenseRecord.month <= end_month)
    records = q.order_by(ExpenseRecord.id).all()

    mem = BytesIO()
    c = canvas.Canvas(mem, pagesize=letter)
    width, height = letter
    x = 40
    y = height - 40
    c.setFont('Helvetica-Bold', 14)
    c.drawString(x, y, f'Fleet Expense Report - {vehicle.name}')
    c.setFont('Helvetica', 9)
    y -= 20
    header = ['ID','Month','Member','Credit','Profit']
    c.drawString(x, y, ' | '.join(header))
    y -= 12
    for r in records:
        line = f"{r.id} | {r.month} | {r.member.name if r.member else ''} | {r.company_credit:.2f} | {r.total_profit_after_tax:.2f}"
        c.drawString(x, y, line)
        y -= 12
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    mem.seek(0)
    filename = f"fleet_report_{vehicle.name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(mem, mimetype='application/pdf', download_name=filename, as_attachment=True)


@app.route('/api/charts')
def charts_api():
    """API endpoint for chart data - returns profit/loss data for each vehicle"""
    vehicles = Vehicle.query.all()
    chart_data = {}
    
    for v in vehicles:
        records = ExpenseRecord.query.filter_by(vehicle_id=v.id).all()
        
        # Calculate totals
        company_credit = sum(r.company_credit or 0 for r in records)
        tds = sum(r.tds_1_percent or 0 for r in records)
        maintenance = sum(r.maintenance or 0 for r in records)
        driver_salary = sum(r.driver_salary or 0 for r in records)
        vehicle_maint = sum(r.vehicle_maintenance or 0 for r in records)
        cng_gas = sum(r.cng_gas or 0 for r in records)
        petrol = sum(r.petrol or 0 for r in records)
        supervisor_comm = sum(r.supervisor_commission or 0 for r in records)
        total_deduction = sum(r.total_deduction or 0 for r in records)
        total_profit = sum(r.total_profit_after_tax or 0 for r in records)
        
        chart_data[f'vehicle_{v.id}'] = {
            'id': v.id,
            'name': v.name,
            'labels': ['Company Credit', 'TDS (1%)', 'Maintenance', 'Driver Salary', 
                      'Vehicle Maint', 'CNG Gas', 'Petrol', 'Supervisor Comm', 'Total Deduction', 'Net Profit'],
            'data': [
                round(company_credit, 2),
                round(tds, 2),
                round(maintenance, 2),
                round(driver_salary, 2),
                round(vehicle_maint, 2),
                round(cng_gas, 2),
                round(petrol, 2),
                round(supervisor_comm, 2),
                round(total_deduction, 2),
                round(total_profit, 2)
            ],
            'summary': {
                'total_credit': round(company_credit, 2),
                'total_deduction': round(total_deduction, 2),
                'total_profit': round(total_profit, 2),
                'record_count': len(records)
            }
        }
    
    return {'vehicles': chart_data}


def _get_prev_month():
    now = datetime.utcnow()
    year = now.year
    month = now.month - 1
    if month == 0:
        month = 12
        year -= 1
    return f"{year}-{month:02d}"


def compose_monthly_summary(month=None):
    if not month:
        month = _get_prev_month()
    vehicles = Vehicle.query.all()
    total_credit = 0.0
    total_deduction = 0.0
    total_profit = 0.0
    per_vehicle = []
    for v in vehicles:
        recs = ExpenseRecord.query.filter(ExpenseRecord.vehicle_id == v.id, ExpenseRecord.month == month).all()
        if not recs:
            continue
        vc = sum((r.company_credit or 0) for r in recs)
        vd = sum((r.total_deduction or 0) for r in recs)
        vp = sum((r.total_profit_after_tax or 0) for r in recs)
        total_credit += vc
        total_deduction += vd
        total_profit += vp
        per_vehicle.append((v.name, vc, vd, vp, len(recs)))

    lines = [f"Fleet Monthly Summary for {month}", "", f"Total Company Credit: {total_credit:.2f}", f"Total Deductions: {total_deduction:.2f}", f"Total Profit After Tax: {total_profit:.2f}", "", "Per vehicle:"]
    for name, vc, vd, vp, cnt in per_vehicle:
        lines.append(f"- {name}: records={cnt}, credit={vc:.2f}, deduction={vd:.2f}, profit={vp:.2f}")
    if not per_vehicle:
        lines.append("No records for the specified month.")
    body = "\n".join(lines)
    return month, body


def get_setting(key, default=None):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s else os.environ.get(key) or default


def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if not s:
        s = Setting(key=key, value=value)
        db.session.add(s)
    else:
        s.value = value
    db.session.commit()


def _attach_file_to_msg(msg, filename, data, mimetype):
    from email.mime.base import MIMEBase
    from email import encoders
    maintype, subtype = mimetype.split('/', 1)
    part = MIMEBase(maintype, subtype)
    part.set_payload(data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(part)


def send_email(subject, body, recipients, attachments=None):
    # attachments: list of tuples (filename, bytes, mimetype)
    smtp_host = get_setting('SMTP_HOST')
    smtp_port = int(get_setting('SMTP_PORT', '587'))
    smtp_user = get_setting('SMTP_USER')
    smtp_pass = get_setting('SMTP_PASS')
    email_from = get_setting('EMAIL_FROM') or smtp_user
    if not smtp_host or not recipients:
        return False, 'SMTP_HOST or recipients not configured'

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for filename, data, mimetype in attachments:
            _attach_file_to_msg(msg, filename, data, mimetype)

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        server.starttls()
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        server.sendmail(email_from, recipients, msg.as_string())
        server.quit()
        return True, 'Email sent'
    except Exception as e:
        return False, str(e)


def send_monthly_summary_job(month=None):
    month, body = compose_monthly_summary(month)
    recipients_setting = get_setting('EMAIL_TO')
    if not recipients_setting:
        return False, 'EMAIL_TO not set'
    recipients = [r.strip() for r in recipients_setting.split(',') if r.strip()]
    subject = f'Fleet Monthly Summary - {month}'

    # Build CSV attachment (all records for month)
    si = io.StringIO()
    writer = csv.writer(si)
    header = ['id','month','vehicle','member','single_way_km','double_way_km','single_total_cost','double_total_cost','tds_1_percent','maintenance','driver_salary','vehicle_maintenance','cng_gas','petrol','supervisor_commission','company_credit','total_deduction','total_profit_after_tax']
    writer.writerow(header)
    recs = ExpenseRecord.query.filter(ExpenseRecord.month == month).order_by(ExpenseRecord.id).all()
    for r in recs:
        writer.writerow([
            r.id, r.month, r.vehicle.name if r.vehicle else '', r.member.name if r.member else '',
            r.single_way_km, r.double_way_km, r.single_total_cost, r.double_total_cost,
            r.tds_1_percent, r.maintenance, r.driver_salary, r.vehicle_maintenance,
            r.cng_gas, r.petrol, r.supervisor_commission, r.company_credit,
            r.total_deduction, r.total_profit_after_tax
        ])
    csv_bytes = si.getvalue().encode('utf-8')

    # Save CSV to exports/ for record-keeping (do not attach to email)
    try:
        exports_dir = os.path.join(os.getcwd(), 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        csv_path = os.path.join(exports_dir, f'fleet_records_{month}.csv')
        with open(csv_path, 'wb') as fh:
            fh.write(csv_bytes)
    except Exception:
        pass

    # Build a single combined PDF for all vehicles
    vehicles = Vehicle.query.all()
    mem_pdf = BytesIO()
    c = canvas.Canvas(mem_pdf, pagesize=letter)
    width, height = letter
    x = 40
    y = height - 40
    c.setFont('Helvetica-Bold', 16)
    c.drawString(x, y, f'Fleet Combined Expense Report - {month}')
    c.setFont('Helvetica', 9)
    y -= 24
    for v in vehicles:
        v_recs = ExpenseRecord.query.filter(ExpenseRecord.vehicle_id == v.id, ExpenseRecord.month == month).order_by(ExpenseRecord.id).all()
        if not v_recs:
            continue
        c.setFont('Helvetica-Bold', 12)
        c.drawString(x, y, f'Vehicle: {v.name} (records: {len(v_recs)})')
        y -= 14
        c.setFont('Helvetica', 9)
        c.drawString(x, y, 'ID | Month | Member | Credit | Profit')
        y -= 12
        for r in v_recs:
            line = f"{r.id} | {r.month} | {r.member.name if r.member else ''} | {r.company_credit:.2f} | {r.total_profit_after_tax:.2f}"
            c.drawString(x, y, line)
            y -= 12
            if y < 60:
                c.showPage()
                y = height - 40
        y -= 10
        if y < 60:
            c.showPage()
            y = height - 40
    c.save()
    mem_pdf.seek(0)
    pdf_bytes = mem_pdf.read()

    # Attach only the combined PDF (no CSV)
    attachments = [
        (f'fleet_report_{month}.pdf', pdf_bytes, 'application/pdf')
    ]

    return send_email(subject, body, recipients, attachments=attachments)


@app.route('/send_summary')
def send_summary():
    month = request.args.get('month')
    ok, msg = send_monthly_summary_job(month)
    if ok:
        flash('Monthly summary sent', 'success')
    else:
        flash(f'Failed to send summary: {msg}', 'danger')
    return redirect(url_for('index'))


# Start scheduler to run monthly on the 1st at 00:05 UTC
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: send_monthly_summary_job(), 'cron', day='1', hour='0', minute='5')
scheduler.start()


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        for key in ['SMTP_HOST','SMTP_PORT','SMTP_USER','SMTP_PASS','EMAIL_FROM','EMAIL_TO']:
            val = request.form.get(key)
            if val is None:
                val = ''
            set_setting(key, val)
        flash('Settings saved', 'success')
        return redirect(url_for('settings'))

    config = {}
    for key in ['SMTP_HOST','SMTP_PORT','SMTP_USER','SMTP_PASS','EMAIL_FROM','EMAIL_TO']:
        config[key] = get_setting(key, '')
    return render_template('settings.html', config=config)


if __name__ == '__main__':
    # ensure DB exists
    if not os.path.exists('expenses.db'):
        with app.app_context():
            db.create_all()
    
    # Generate SSL certificate if it doesn't exist
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        print("Generating self-signed SSL certificate...")
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generate private key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "LocalHost"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Self-Signed"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
            ]),
            critical=False,
        ).sign(key, hashes.SHA256(), default_backend())
        
        # Save certificate
        with open('cert.pem', 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Save private key
        with open('key.pem', 'wb') as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print("SSL certificate generated!")
    
    # Run on all network interfaces with HTTPS
    print("Starting HTTPS server...")
    print("Access your app at: https://<your-ip-address>:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
