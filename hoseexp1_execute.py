from openhubo import comps
import openhubo
import time

from openravepy import RaveCreateProblem
from numpy import pi
import openravepy as rave
import utilities_hao as hao

#match to planner
#TODO: store this in a config file of some sort...
from hoseexp1_plan import useArm

(env,options)=openhubo.setup('qtcoin')
options.scenefile='scenes/hoseexp1.env.xml'
if options.physics is None:
    options.physics=True

[robot,ctrl,ind,ghost,recorder]=openhubo.load_scene(env,options)
#initialization
hydrant_horizontal = env.GetKinBody('hydrant_horizontal')
hydrant_vertical = env.GetKinBody('hydrant_vertical')
hose = env.GetKinBody('hose')
hose.Enable(False)

basemanip = rave.interfaces.BaseManipulation(robot)
prob_manip = RaveCreateProblem(env,'Manipulation')
env.LoadProblem(prob_manip,robot.GetName())

env.StartSimulation(openhubo.TIMESTEP)

hao.RunOpenRAVETraj(robot, 'grasphose.traj')

robot.SetActiveManipulator(robot.GetManipulators()[useArm])
robot.Grab(hose)
hose.Enable(True)
hao.closeHand(robot,useArm,pi/4)
time.sleep(3)

hao.RunOpenRAVETraj(robot, 'moveup.traj')
robot.WaitForController(0)
hao.RunOpenRAVETraj(robot, 'attachhose.traj')
robot.WaitForController(0)
hao.RunOpenRAVETraj(robot, 'insert.traj')
robot.WaitForController(0)
