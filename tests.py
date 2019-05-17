import SmarAct
import unittest

class movementTests(unittest.TestCase):

    def setUp(self):
        print('/n Setting up next test.../n')
        self.sampleStage_IP = 'network:192.168.1.201:5000'
        self.focusStage_IP = 'network:192.168.1.200:5000'
        self.port = 5000
        self.SA = SmarAct.SmarAct()
        print(self.SA.GetDLLVersion())
        result, self.controllerHandle = self.SA.OpenSystem(self.focusStage_IP, 'sync')
        print(result)
        if result == 0:
            print('Controller connected.')
        result, c = self.SA.GetNumberOfChannels(self.controllerHandle)
        print('Controller has ' + str(c) + ' channels.')
        self.numChannels = c

    def PositionKnown(self):
        print('Does the controller know its position?')
        for i in range(self.numChannels):
            print('Axis: ' + str(i))
            result, posKnown = self.SA.GetPhysicalPositionKnown_S(self.controllerHandle, i)
            self.assertEqual(result,0)
            print('Status ' + str(result) + ', and position known status is: ' + str(posKnown))
            self.getSafeDir(i)

    def testCalibrateEffects(self):
        print('Test effect of cal on position known')
        self.PositionKnown()
        for i in range(self.numChannels):
            result = self.SA.CalibrateSensor_S(self.controllerHandle, i)
            self.assertEqual(result, 0)
            print('Channel ' + str(i) + ' calibrated.')
            ret = self.SA.FindReferenceMark_S(self.controllerHandle, i, 0, 0, 0)
            print('Went to reference with status ' + str(ret))
        self.PositionKnown()

    def testSensorPowercycle(self):
        print('Testing the effect of sensor power cycle on position known')
        self.testCalibrateEffects()
        self.sensorStatus()
        result = self.SA.SetSensorEnabled_S(self.controllerHandle,0)
        print('Sensors turned off with result ' + str(result))
        self.sensorStatus()
        self.PositionKnown()
        result = self.SA.SetSensorEnabled_S(self.controllerHandle, 1)
        print('Sensors turned on with result ' + str(result))
        self.PositionKnown()

    def testRefAutoZero(self):
        print('tests for AutoZero option of find ref point')
        for i in range(self.numChannels):
            ret = self.SA.GotoPositionRelative_S(self.controllerHandle, i, 5000000, 0)
            pos = self.SA.GetPosition_S(self.controllerHandle, i)
            print("axis channel " + str(i) + 'has moved to pos ' + str(pos) + ' with error code ' + str(ret))
            ret = self.SA.SetPosition_S(self.controllerHandle, i, 400000000000000)
            pos = self.SA.GetPosition_S(self.controllerHandle, i)
            print("position is changed to: " + str(pos) + ' with error code ' + str(ret))
            print('assuming non-auto-zero is 0')
            ret = self.SA.FindReferenceMark_S(self.controllerHandle, i, 0,0,0)
            pos = self.SA.GetPosition_S(self.controllerHandle, i)
            print("position is changed to: " + str(pos) + ' with error code ' + str(ret))
            print('assuming auto-zero is 1')
            ret = self.SA.FindReferenceMark_S(self.controllerHandle, i, 0,0,1)
            pos = self.SA.GetPosition_S(self.controllerHandle, i)
            print("position is changed to: " + str(pos) + ' with error code ' + str(ret))

    def sensorStatus(self):
        r, s = self.SA.GetSensorEnabled_S(self.controllerHandle)
        if r == 0:
            print(str(s))
        else:
            print('error ', r)

    def getSafeDir(self, channel):
        r, d = self.SA.GetSafeDirection_S(self.controllerHandle, channel)
        if r == 0:
            print('Safe direction is ' + str(d))
        else:
            print('Could not find safe direction, error ' + str(r))
            try:
                print(self.SA.FunctionStatusCodes[r])
            except:
                pass

    def tearDown(self):
        self.SA.CloseSystem(self.controllerHandle)


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()