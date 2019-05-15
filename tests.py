import SmarAct
import unittest

class movementTests(unittest.TestCase):

    def __init__(self):
        super.__init__()
        self.sampleStage_IP = 192.168.1.201
        self.focusStage_IP = 192.168.1.200
        self.port = 5000


    def setUp(self):
        self.SA = SmarAct.SmarAct()
        print(self.SA.GetDLLVersion())

    def testInitConnection(self):
        input("Connect ethernet to leftmost controller and press enter")
        result, self.controllerHandle = self.SA.OpenSystem(self.focusStage_IP, 'sync')
        self.assertEqual(result, 0)



    def tearDown(self):
        pass
        #self.SA.CloseSystem()


if __name__ == '__main__':
    unittest.main()