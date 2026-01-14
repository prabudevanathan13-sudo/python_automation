from turtle import *
speed(0)
bgcolor('black')
colors=['green','red']
hideturtle()
for i in range(122):
    
    
    goto(0,0)
    color(colors[1%2])
    forward(130)
    left(3)
    circle(40)
    forward(130)
    right(180)
done()
