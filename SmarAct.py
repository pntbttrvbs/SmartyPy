from ctypes import *
import sys
import platform

class SmarAct:
    def __init__(self):
        if sys.platform == 'linux2':
            dllname = '/usr/local/path/to/smaract'
            self.dll = cdll.LoadLibrary(dllname)
        elif sys.platform == 'win32':
            if platform.architecture()[0] == '64bit' :
                dllname = 'C:\SmarAct\MCS\SDK\lib64\MCSControl.dll'
            else:
                dllname = 'C:\SmarAct\MCS\SDK\lib\MCSControl.dll'
            self.dll = windll.LoadLibrary(dllname)
        else:
            print("Cannot detect OS.")
            raise


    def AddSystemToInitSystemsList(self):
        #depricated function
        pass

    def CloseSystem(self, systemIndex):
        '''
        Interface:

        SA_STATUS SA_CloseSystem(SA_INDEX systemIndex)

        Description:

        This function closes a system initialized with SA_OpenSystem. It should be called before the application closes.
        Calling this function makes the acquired systems available to other applications again. It is important to close
        initialized systems. Not closed systems will cause a resource leak. An attempt to open an unclosed MCS again
        will fail because the connection is still hold by the previous initialization.

        SA_CloseSystem does not close systems that have been initialized with SA_InitSystems.

        Parameters:

        systemIndex (SA_INDEX), input – A handle to the system which will be closed.

        Example:

        unsigned int mcsHandle;
        const char loc[] = “usb:id:3118167233”;
        SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
        if(result == SA_OK){
            //Closing previously aquired system
            SA_CloseSystem(mcsHandle);
        }

        See also: SA_OpenSystem, SA_GetSystemLocator, SA_Fi

        '''
        c_systemIndex = c_uint32(systemIndex)
        ret = self.dll.SA_CloseSystem(c_systemIndex)
        return (ret)

    def ClearInitSystemsList(self):
        #depricated
        pass

    def FindSystems(self, options, ioBufferSize):

        '''

        Interface:

        SA_STATUS SA_FindSystems(const char *options,
                                 char *outBuffer,
                                 unsigned int *ioBufferSize);

        Description:

        This function writes a list of locator strings of MCS devices that are connected to the PC into outBuffer.
        Currently the function only lists MCS with a USB interface. Options contains a list of configuration options
        for the find procedure (currently unused). The caller must pass a pointer to a char buffer in outBuffer and set
        ioBufferSize to the size of the buffer. After the call the function has written a list of system locators into
        outBuffer and the number of written bytes into ioBufferSize. If the supplied buffer is too small to contain the
        generated list, the buffer will contain no valid content but ioBufferSize contains the required buffer size.

        Parameters:
            options (const char), input – Options for the find procedure. Currently unused.
            outBuffer (char), output – Pointer to a buffer which holds the device locators after the function has
            returned
            ioBufferSize (unsigned int), input/output – Specifies  the size of outBuffer before the function call.
            After the function call it holds the number of bytes written to outBuffer.

        Example:

        char outBuffer[4096];
        unsigned int bufferSize = sizeof(outBuffer);
        SA_STATUS result = SA_FindSystems(“”, outBuffer, &bufferSize);
        if(result == SA_OK){
            // outBuffer holds the locator strings, separated by '\n'
            // bufferSize holds the number of bytes written to outBuffer
        }

        See also:Initialization, SA_OpenSyste
        '''

        c_options = c_char(options)
        c_outBuffer = create_string_buffer(ioBufferSize)
        c_ioBufferSize = c_uint(ioBufferSize)

        ret = self.dll.SA_FindSystems(c_options, c_outBuffer, byref(c_ioBufferSize))
        return (ret, c_outBuffer.value, c_ioBufferSize.value)


    def GetAvailableSystems(self):
        #depricated
        pass


    def GetChannelType(self, systemIndex, channelIndex):

        '''

        Interface:

        SA_STATUS SA_GetChannelType(SA_INDEX systemIndex,
                                    SA_INDEX channelIndex,
                                    unsigned int *type);

        Description:

        This function may be used to determine the type of a channel of a system. Each channel of a system has a
        specific type. Currently there are two types of channels: positioner channels and end effector channels. Most
        functions of section II are only callable for certain channel types. The function descriptions list for which
        types they may be called.

        Parameters:
            systemIndex (unsigned 32bit), input -  Handle to an initialized system.
            channelIndex (unsigned 32bit), input - Selects the channel of the selected system. The index is zero based.
            type (unsigned 32bit), output - If the call was successful this parameter holds the channel type of the
            selected channel. Possible values are SA_POSITIONER_CHANNEL_TYPE and SA_END_EFFECTOR_CHANNEL_TYPE.
        #TODO: check on those two value possibilities.

        Example:

        unsigned int mcsHandle;
        const char loc[] = “usb:id:3118167233”;
        SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
        if (result != SA_OK) {
            // handle error...
        }
        unsigned int type;
        result = SA_GetChannelType(mcsHandle,0,&type);
        if (result == SA_OK) {
            // type holds the channel type of the first channel of the first system
        }
        '''

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_type = c_uint32()
        ret = self.dll.SA_GetChannelType(c_systemIndex, c_channelIndex, byref(c_type))
        return (ret, c_type.value)

    def GetDLLVersion(self):

        '''
        Interface:

        SA_STATUS SA_GetDLLVersion(unsigned int *version);

        Description:

        This function may be called to retrieve the version code of the library. It is useful to check if changes have
        been made to the software interface. An application may check the version in order to ensure that the library
        behaves as the application expects it to do.The returned 32bit code is divided into three fields:
        31     24 | 23     16 | 15     8 | 7      0
        Version High | Version Low | Version Build

        This function does not require the library to be initialized (see SA_OpenSystem) and will always return a status
        code of SA_OK.

        Parameters:
            version (unsigned 32bit), output - Holds the version code. The higher the value the newer the version.

        Example:

        unsigned int version;
        SA_GetDLLVersion(&version)
        :return:
        '''

        c_version = c_uint32()
        ret = self.dll.SA_GetDLLVersion(byref(c_version))
        return (ret, c_version.value)


    def GetInitState(self):
        #depricated
        pass


    def GetNumberOfChannels(self, systemIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channels = c_uint32()

        ret = self.dll.SA_GetNumberOfChannels(c_systemIndex, byref(c_channels))
        return(ret, c_channels)

    def GetNumberOfSystems(self):
        #depricated
        pass

    def GetSystemId(self):
        #depricated
        pass

    def GetSystemLocator(self, systemIndex, ioBufferSize):

        c_systemIndex = c_uint32(systemIndex)
        c_outBuffer = create_string_buffer(ioBufferSize)
        c_ioBufferSize = c_uint(ioBufferSize)

        ret = self.dll.SA_GetSystemLocator(c_systemIndex, c_outBuffer, byref(c_ioBufferSize))
        return (ret, c_outBuffer.value, c_ioBufferSize.value)

    def InitSystems(self):
        #depricated
        pass

    def OpenSystem(self, systemLocator, options):
        """
        Interface:

        SA_STATUS SA_OpenSystem(SA_INDEX *systemIndex,
                                const char *systemLocator,
                                const char *options);

        Description:
        Initializes one MCS specified in systemLocator, systemIndex is a handle to the opened system that is returned
        after a successful execution. It must be passed in the systemIndex parameter to the API functions. options is a
        string parameter that contains a list of configuration options. The options must be separated by a comma or a
        newline.

        The following options are available:
            reset           the MCS is reset on open. A reset has the same effect as a power-down/power-up cycle.
            async, sync     use the async option to set the communication mode to asynchronous, sync for synchronous
                            communication. See “Communication Modes“ on p.8.
            open-timeout <t>only available for network interfaces. <t> is the maximum time in milliseconds the PC
                            tries to connect to the MCS. Default is 3000 milliseconds. The maximum timeout may be
                            limited by operating system default parameters.

        Systems that have been initialized with SA_OpenSystem must be released with SA_CloseSystem. SA_ReleaseSystems
         oes not close them!

        Parameters:

            systemIndex (SA_INDEX), output – returns a handle to the opened system.
            systemLocator (const char pointer), input – locator string that specifies the system.
            options (const char pointer), input – options for the initialization function. See list above.

        Example:

            const char loc1[] = “usb:id:3118167233”;
            const char loc2[] = “network:192.168.1.200:5000”;

            SA_STATUS result;
            SA_INDEX mcsHandle1,mcsHandle2;

            // connect to a USB interface for async. communication and reset the system
            result = SA_OpenSystem(&mcsHandle1, loc1, “async,reset”);
            if(result != SA_OK){
                // handle error
            }
            // connect to a network interface for sync. communication with 1.5 sec timeout
            result = SA_OpenSystem(&mcsHandle2, loc2, “sync,open-timeout 1500”);
            if(result != SA_OK){
                // handle error
            }

            See also:SA_FindSystems, SA_GetSystemLocator, SA_CloseSyste
        """
        c_systemIndex = c_uint32()
        systemLocator_bytes = systemLocator.encode()
        c_systemLocator = c_char_p(systemLocator_bytes)
        print(c_systemLocator)
        c_options = c_wchar_p(options)

        ret = self.dll.SA_OpenSystem(byref(c_systemIndex), c_systemLocator, c_options)
        return (ret, c_systemIndex.value)

    def ReleaseSystems(self):
        #depricated
        pass

    def SetHCMEnabled(self, systemIndex, enabled):

        c_systemIndex = c_uint32(systemIndex)
        c_enabled = c_uint32(enabled)

        ret = self.dll.SA_SetHCMEnabled(c_systemIndex, c_enabled)
        return (ret)


    #Functions for Synchronous Communication

    def CalibrateSensor_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)

        ret = self.dll.SA_CalibrateSensor_S(c_systemIndex, c_channelIndex)

    def FindReferenceMark_S(self, systemIndex, channelIndex, direction, holdTime, autoZero):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_direction = c_uint32(direction)
        c_holdTime = c_uint32(holdTime)
        c_autoZero = c_uint32(autoZero)

        ret = self.dll.SA_FindReferenceMark_S(c_systemIndex, c_channelIndex, c_direction, c_holdTime, c_autoZero)
        return (ret)

    def GetAngle_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_angle = c_uint32()
        c_revolution = c_int32()

        ret = self.dll.SA_GetAngle_S(c_systemIndex,c_channelIndex,byref(c_angle),byref(c_revolution))
        return (ret,c_angle.value,c_revolution.value)

    def GenAngleLimit_S(self):
        pass

    def GetCaptureBuffer_S(self, systemIndex,channelIndex,bufferIndex):
        pass

    def GetChannelProperty_S(self, systemIndex, channelIndex, key):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_key = c_uint32(key)
        c_value = c_int32()

        ret = self.dll.SA_GetChannelProperty_S(c_systemIndex, c_channelIndex, c_key, byref(c_value))
        return (ret, c_value.value)

    def GetClosedLoopMoveAcceleration_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_acceleration = c_uint32()

        ret = self.dll.SA_GetClosedLoopMoveAcceleration_S(c_systemIndex, c_channelIndex, byref(c_acceleration))
        return (ret, c_acceleration)

    def GetClosedLoopMoveSpeed_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_speed = c_uint32()

        ret = self.dll.SA_GetClosedLoopMoveAcceleration_S(c_systemIndex, c_channelIndex, byref(c_speed))
        return (ret, c_speed)

    def GetEndEffectorType_S(self):
        pass

    def GetForce_S(self):
        pass

    def GetGripperOpening_S(self):
        pass

    def GetPhysicalPositionKnown_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_known = c_uint32()

        ret = self.dll.SA_GetPhysicalPositionKnown_S(c_systemIndex, c_channelIndex, byref(c_known))
        return (ret, c_known)

    def GetPosition_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_position = c_uint32()

        ret = self.dll.SA_GetPhysicalPositionKnown_S(c_systemIndex, c_channelIndex, byref(c_position))
        return (ret, c_position)

    def GetPositionLimit_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_minPosition = c_uint32()
        c_maxPosition = c_uint32()

        ret = self.dll.SA_GetPositionLimit_S(c_systemIndex, c_channelIndex, byref(c_minPosition), byref(c_maxPosition))
        return (ret, c_minPosition.value, c_maxPosition.value)

    def GetSafeDirection_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_direction = c_uint32()

        ret = self.dll.SA_GetSafeDirection_S(c_systemIndex, c_channelIndex, byref(c_direction))
        return (ret, c_direction.value)

    def GetScale_S(self, systemIndex, channelIndex):
        pass

    def GetSensorEnabled_S(self, systemIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_enabled = c_uint32()

        ret = self.dll.SA_GetSensorEnabled_S(c_systemIndex, byref(c_enabled))
        return (ret, c_enabled.value)

    def GetSensorType_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_type = c_uint32()

        ret = self.dll.SA_GetSensorType_S(c_systemIndex, c_channelIndex, byref(c_type))
        return (ret, c_type.value)

    def GetStatus_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_status = c_uint32()

        ret = self.dll.SA_GetStatus_S(c_systemIndex, c_channelIndex, byref(c_status))
        return (ret, c_status.value)

    def GetVoltageLevel_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_level = c_uint32()

        ret = self.dll.SA_GetVoltageLevel_S(c_systemIndex, c_channelIndex, byref(c_level))
        return (ret, c_level.value)

    def GotoAngleAbsolute_S(self):
        pass

    def GotoAngleRelative_S(self):
        pass

    def GotoGripperForceAbsolute_S(self):
        pass

    def GotoGripperOpenAbsolute_S(self):
        pass

    def GotoGripperOpeningRelative_S(self):
        pass

    def GotoPositionAbsolute_S(self, systemIndex, channelIndex, position, holdTime):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_position = c_int32(position)
        c_holdTime = c_uint32(holdTime)

        ret = self.dll.SA_GotoPositionAbsolute_S(c_systemIndex, c_channelIndex, c_position, c_holdTime)
        return (ret)

    def GotoPositionRelative_S(self, systemIndex, channelIndex, diff, holdTime):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_diff = c_int32(diff)
        c_holdTime = c_uint32(holdTime)

        ret = self.dll.SA_GotoPositionAbsolute_S(c_systemIndex, c_channelIndex, c_diff, c_holdTime)
        return (ret)

    def ScanMoveAbsolute_S(self, systemIndex, channelIndex, target, scanSpeed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_target = c_uint32(target)
        c_scanSpeed = c_uint32(scanSpeed)

        ret = self.dll.SA_GotoPositionAbsolute_S(c_systemIndex, c_channelIndex, c_target, c_scanSpeed)
        return (ret)

    def ScanMoveRelative_S(self, systemIndex, channelIndex, diff, scanSpeed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_diff = c_uint32(diff)
        c_scanSpeed = c_uint32(scanSpeed)

        ret = self.dll.SA_GotoPositionAbsolute_S(c_systemIndex, c_channelIndex, c_diff, c_scanSpeed)
        return (ret)

    def SetAccumulateRelativePositions_S(self, systemIndex, channelIndex, accumulate):

        c_systemIndex = c_uint32(systemIndex)
        c_chanelIndex = c_uint32(channelIndex)
        c_accumulate = c_uint32(accumulate)

        ret = self.dll.SA_SetAccumulateRelativePositions_S(c_systemIndex, c_chanelIndex, c_accumulate)

    def SetAngleLimit_S(self):
        pass

    def SetChannelProperty_S(self, systemIndex, channelIndex, key, value):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_key = c_uint32(key)
        c_value = c_int32(value)

        ret = self.dll.SA_GetChannelProperty_S(c_systemIndex, c_channelIndex, c_key, c_value)
        return (ret)

    def SetClosedLoopMaxFrequency_S(self, systemIndex, channelIndex, frequency):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_frequency = c_uint32(frequency)

        ret = self.dll.SA_SetClosedLoopMaxFrequency_S(c_systemIndex, c_channelIndex, c_frequency)
        return (ret)

    def SetClosedLoopMoveAcceleration_S(self, systemIndex, channelIndex, acceleration):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_acceleration = c_uint32(acceleration)

        ret = self.dll.SA_SetClosedLoopMaxFrequency_S(c_systemIndex, c_channelIndex, c_acceleration)
        return(ret)

    def SetClosedLoopMoveSpeed_S(self, systemIndex, channelIndex, speed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_speed = c_uint32(speed)

        ret = self.dll.SA_SetClosedLoopMaxFrequency_S(c_systemIndex, c_channelIndex, c_speed)
        return (ret)

    def SetEndEffectorType_S(self):
        pass

    def SetPosition_S(self, systemIndex, channelIndex, position):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_position = c_int32(position)

        ret = self.dll.SA_SetClosedLoopMaxFrequency_S(c_systemIndex, c_channelIndex, c_position)
        return (ret)

    def SetPositionLimit_S(self, systemIndex, channelIndex, minPosition, maxPosition):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_minPosition = c_int32(minPosition)
        c_maxPosition = c_int32(maxPosition)

        ret = self.dll.SA_SetClosedLoopMaxFrequency_S(c_systemIndex, c_channelIndex, c_minPosition, c_maxPosition)
        return (ret)

    def SetSafeDirection_S(self, systemIndex, channelIndex, direction):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_direction = c_uint32(direction)

        ret = self.dll.GetSafeDirection_S(c_systemIndex, c_channelIndex, c_direction)
        return (ret)

    def SetScale_S(self):
        pass

    def SetSensorEnabled_S(self, systemIndex, enabled):

        c_systemIndex = c_uint32(systemIndex)
        c_enabled = c_uint32(enabled)

        ret = self.dll.SA_SetSensorEnabled_S(c_systemIndex, c_enabled)
        return (ret)

    def SetSensorType_S(self):
        pass

    def SetStepWhileScan_S(self):
        pass

    def SetZeroForce_S(self):
        pass

    def StepMove_S(self, systemIndex, channelIndex, steps, amplitude, frequency):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_steps = c_int32()
        c_frequency = c_uint32()
        c_amplitude = c_uint32()

        ret = self.dll.SA_GetSafeDirection_S(c_systemIndex, c_channelIndex, c_steps, c_frequency, c_amplitude)
        return (ret)

    def Stop_S(self, systemIndex, channelIndex):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)

        ret = self.dll.SA_Stop_S(c_systemIndex, c_channelIndex)
        return (ret)

    #Misc Functions

    def DSV(self, value):

        c_value = c_int32(value)
        c_selector = c_uint32()
        c_subSelector = c_uint32()

        ret = self.dll.SA_DSV(c_value, byref(c_selector), byref(c_subSelector))
        return (ret, c_selector.value, c_subSelector.value)

    def EPK(self, selector, subSelector, property):

        c_selector = c_uint32(selector)
        c_subSelector = c_uint32(subSelector)
        c_property = c_uint32(property)

        ret = self.dll.SA_EPK(c_selector, c_subSelector, c_property)
        return (ret)

    def ESV(self):
        pass

    def GetStatusInfo(self, status):

        c_status = c_uint32(status)
        c_info = create_string_buffer(50)
        ret = self.dll.SA_GetStatusInfo(c_status, c_info)
        return (ret, c_info.value)









