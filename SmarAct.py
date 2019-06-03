from ctypes import *
import sys
import platform

class SmarAct:

    FunctionStatusCodes = {
        0: ('SA_OK', 'The function call was successful.'),
        1: ('SA_INITIALIZATION_ERROR', 'An error occurred while initializing the library. All systems should be '
                                       'disconnected and reset before the next attempt is made.'),
        2: ('SA_NOT_INITIALIZED_ERROR', 'A function call has been made for an uninitialized system. Call SA_OpenSystem '
                                        'before communicating with the hardware.'),
        3: ('SA_NO_SYSTEMS_FOUND_ERROR', 'May occur at initialization if no Modular Control Systems have been detected '
                                         'on the PC system. Check the connection of the USB cable and make sure the '
                                         'drivers are installed properly. Note: After power-up / USB connection it may '
                                         'take several seconds for the system to be detectable.'),
        4: ('SA_TOO_MANY_SYSTEMS_ERROR', 'The number of allowed systems connected to the PC is limited to 32. If you '
                                         'have more connected, disconnect some.'),
        5: ('SA_INVALID_SYSTEM_INDEX_ERROR', 'An invalid system index has been passed to a '
                                                                   'function. The system index parameter of various '
                                                                   'functions is zero based. If N is the number of '
                                                                   'acquired systems, then the valid range for the '
                                                                   'system index is 0..(N-1).'),
        6: ('SA_INVALID_CHANNEL_INDEX_ERROR', 'An invalid channel index has been passed to a function. The channel '
                                              'index parameter of various functions is zero based. If N is the number '
                                              'of channels available on a system, then the valid range for the channel '
                                              'index is 0..(N-1).'),
        7: ('SA_TRANSMIT_ERROR', 'An error occurred while sending data to the hardware. The system should be reset.'),
        8: ('SA_WRITE_ERROR', 'An error occurred while sending data to the hardware. The system should be reset.'),
        9: ('SA_INVALID_PARAMETER_ERROR', 'An invalid parameter has been passed to a function. Check the function '
                                          'documentation for valid ranges.'),
        10: ('SA_READ_ERROR', 'An error occurred while receiving data from the hardware. The system should be reset.'),
        12: ('SA_INTERNAL_ERROR', 'An internal communication error occurred.The system should be reset.'),
        13: ('SA_WRONG_MODE_ERROR', 'The called function does not match the communication mode that was selected at '
                                    'initialization (see2.2.2 – “Communication Modes“).In synchronous communication '
                                    'mode only functions of sections I and IIa may be called.In asynchronous '
                                    'communication mode only functions of sections I and IIb may be called.'),
        14: ('SA_PROTOCOL_ERROR', 'An internal protocol error occurred.The system should be reset.'),
        15: ('SA_TIMEOUT_ERROR', 'The hardware did not respond. Make sure that all cables are connected properly and '
                                 'reset the system.'),
        17: ('SA_ID_LIST_TOO_SMALL_ERROR', 'When calling SA_GetAvailableSystems you must pass a pointer to an array that'
                                           ' is large enough to hold the system IDs of all connected systems. If the '
                                           'number of detected systems is larger than the array, this error will be '
                                           'generated.'),
        18: ('SA_SYSTEM_ALREADY_ADDED_ERROR', 'In order to acquire specific systems you must call '
                                              'SA_AddSystemToInitSystemsList before calling SA_InitSystems. A system ID'
                                              'may only be added once to the list of systems to be acquired. Multiple '
                                              'calls with the same ID lead to this error.'),
        19: ('SA_WRONG_CHANNEL_TYPE_ERROR', 'Most functions of section II are only callable for certain channel types.'
                                            'For example, calling SA_StepMove_S for a channel that is an end effector '
                                            'channel will lead to this error.The detailed function description notes '
                                            'the types of channels that the function may be called for.'),
        20: ('SA_CANCELED_ERROR', 'The functions SA_ReceiveNextPacket_A and SA_LookAtNextPacket_A return this code if '
                                  'they were blocking while waiting for an incoming packet and then were manually '
                                  'unblocked by calling SA_CancelWaitForPacket_A.'),
        21: ('SA_INVALID_SYSTEM_LOCATOR_ERROR', 'Returned by SA_OpenSystem if the locator string does not comply with '
                                                'the supported locator formats.'),
        22: ('SA_INPUT_BUFFER_OVERFLOW_ERROR', 'This error occurs when the input buffer for storing packets that have '
                                               'been received from a system is full. To avoid this error remove packets '
                                               'from the input buffer frequently with SA_ReceiveNextPacket_A.'),
        23: ('SA_QUERYBUFFER_SIZE_ERROR', 'Returned by functions that write data in a binary or char buffer(e.g. '
                                          'SA_FindSystem) if the user - supplied buffer is too small to hold the '
                                          'returned data.'),
        24: ('SA_DRIVER_ERROR', 'Returned by functions, if a driver, that is required to communicate to a controller '
                                'over a certain hardware interface, is not available.'),
        128: ('SA_NO_SUCH_SLAVE_ERROR','An internal communication error occurred.The system should be reset.'),
        129: ('SA_NO_SENSOR_PRESENT_ERROR', 'This error occurs if a function was called that requires sensor feedback, '
                                            'but the addressed positioner has none attached.'),
        130: ('SA_AMPLITUDE_TOO_LOW_ERROR', 'The amplitude parameter that was given is too low.'),
        131: ('SA_AMPLITUDE_TOO_HIGH_ERROR', 'The amplitude parameter that was given is too high.'),
        132: ('SA_FREQUENCY_TOO_LOW_ERROR', 'The frequency parameter that was given is too low.'),
        133: ('SA_FREQUENCY_TOO_HIGH_ERROR', 'The frequency parameter that was given is too high.'),
        135: ('SA_SCAN_TARGET_TOO_HIGH_ERROR', 'The target position for a scanning movement that was given is too high.'),
        136: ('SA_SCAN_SPEED_TOO_LOW_ERROR', 'The scan speed parameter that was given for a scan movement command is too low.'),
        137: ('SA_SCAN_SPEED_TOO_HIGH_ERROR', 'The scan speed parameter that was given for a scan movement command is too high.'),
        140: ('SA_SENSOR_DISABLED_ERROR', 'This error occurs if an addressed positioner has a sensor attached, but is disabled. See SA_SetSensorEnabled_S.')
    }
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

        :param systemIndex (SA_INDEX):, input – A handle to the system which will be closed.

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
            :param options: (const char), input – Options for the find procedure. Currently unused.
            outBuffer (char), output – Pointer to a buffer which holds the device locators after the function has
                returned
            :param ioBufferSize: (unsigned int), input/output – Specifies  the size of outBuffer before the function call.
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
            :param systemIndex: (unsigned 32bit), input -  Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is zero based.
            :return type: (unsigned 32bit), output - If the call was successful this parameter holds the channel type of the
            selected channel. Possible values are SA_POSITIONER_CHANNEL_TYPE and SA_END_EFFECTOR_CHANNEL_TYPE.


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
        return(ret, c_channels.value)

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

            :return systemIndex: (SA_INDEX), output – returns a handle to the opened system.
            :param systemLocator: (const char pointer), input – locator string that specifies the system.
            :param options: (const char pointer), input – options for the initialization function. See list above.

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
        c_options = c_wchar_p(options)

        ret = self.dll.SA_OpenSystem(byref(c_systemIndex), c_systemLocator, c_options)
        return (ret, c_systemIndex.value)

    def ReleaseSystems(self):
        #depricated
        pass

    def SetHCMEnabled(self, systemIndex, enabled):

        """
        Description:
        This function may be used to enable or disable a Hand Control Module that is attached to the system to avoid
        interference while the software is in control of the system.
        """

        c_systemIndex = c_uint32(systemIndex)
        c_enabled = c_uint32(enabled)

        ret = self.dll.SA_SetHCMEnabled(c_systemIndex, c_enabled)
        return (ret)


    #Functions for Synchronous Communication

    def CalibrateSensor_S(self, systemIndex, channelIndex):

        """
        Channel type: Positioner

        Interface:
        SA_STATUS SA_CalibrateSensor_S(SA_INDEX systemIndex,
                                       SA_INDEX channelIndex);

        Description:
        This function may be used to increase the accuracy of the position calculation. It is only executable by a
        positioner that has a sensor attached to it. The sensor must also be enabled or in power save mode (see
        SA_SetSensorEnabled_S). If this is not the case the channel will return an error.

        This function should be called once for each channel if the mechanical setup changes (different positioners
        connected to different channels). The calibration data will be saved to non-volatile memory. If the mechanical
        setup is unchanged, it is not necessary to call this function on each initialization, but newly connected
        positioners have to be calibrated in order to ensure proper operation.

        During the calibration the positioner will perform a movement of up to several mm. You must ensure, that the
        command is not executed while the positioner is near a mechanical end stop. Otherwise the calibration mightfail
        and lead to unexpected behavior when executing closed-loop commands. As a safety precaution, also make sure
        that the positioner has enough freedom to move without damaging other equipment.

        The calibration takes a few seconds to complete. During this time the positioner will report a status of
        SA_CALIBRATING_STATUS (see SA_GetStatus_S).

        Positioners that are referenced via a mechanical end stop (see 5.4 “Sensor Types“) are moved to the end stop as
        part of the calibration routine. Which end stop is used for referencing is configured bySA_SetSafeDirection_S.
        Note that when changing the safe direction the end stop must be calibrated again for proper operation.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is zero based.

        Example:
            unsigned int mcsHandle;
            const char loc[] = “usb:id:3118167233”;
            SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
            if (result != SA_OK) {
                // handle error...
            }
            // start calibration routine
            result = SA_CalibrateSensor_S(mcsHandle,0);
            unsigned int status;
            do {
                SA_GetStatus_S(mcsHandle,0,&status);
            } while (status != SA_STOPPED_STATUS);
            // done calibrating



        """

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)

        ret = self.dll.SA_CalibrateSensor_S(c_systemIndex, c_channelIndex)
        return (ret)

    def FindReferenceMark_S(self, systemIndex, channelIndex, direction, holdTime, autoZero):

        """
        Channel type: Positioner

        Interface:SA_STATUS SA_FindReferenceMark_S(SA_INDEX systemIndex,
                                                   SA_INDEX channelIndex,
                                                   unsigned int direction,
                                                   unsigned int holdTime,
                                                   unsigned int autoZero);

        Description:
        For positioners that are equipped with sensor feedback, this function may be used to move the positioner to a
        known physical position of the positioner. Some sensor types are equipped with a physical reference mark,
        others are referenced via a mechanical end stop (see appendix 5.4 “Sensor Types“). For latter types you must
        configure the safe direction with SA_SetSafeDirection_S and call SA_CalibrateSensor_S before the positioner can
        be properly referenced. The safe direction is then used instead of the direction parameter described below.

        If the auto zero flag is set, the current position resp. angle is set to zero after the reference position has
        been reached. Otherwise the position is set according to the information stored in non-volatile memory of the
        last SA_SetPosition_S call. See section 2.5.3 “Defining Positions“ for more information.

        As a safety precaution, make sure that the positioner has enough freedom to move without damaging other
        equipment.

        The positioner may be instructed to hold the position of the reference mark after it has been reached. This
        behavior is similar to that of the other closed-loop commands, e.g. SA_GotoPositionAbsolute_S. See there for
        more information.

        While executing the command the positioner will have a movement status of SA_FINDING_REF_STATUS. While holding
        the position the positioner will have a movement status of SA_HOLDING_STATUS (seeSA_GetStatus_S).

        If this command was successful, then the physical position of the positioner becomes known.
        See SA_GetPhysicalPositionKnown_S.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the system. The index is zero based.
            :param direction: (unsigned 32bit), input - Specifies the initial search direction.
                (See Table in 2.5.3 Defining Positions for valid values and explanations). Note that this parameter is
                ignored for sensor types that are referenced via a mechanical end stop. Set the direction via
                SA_SetSafeDirection_S instead.
            :param holdTime: (unsigned 32bit), input - Specifies how long (in milliseconds) the position is actively
                held after reaching the target. The valid range is 0..60,000. A 0 deactivates this feature, a value of
                60,000 is infinite (until manually stopped, see SA_Stop_S).
            :param autoZero: (unsigned 32bit), input - Must be one of SA_NO_AUTO_ZERO (0) or SA_AUTO_ZERO (1). The
                latter will reset the current position resp. angle to zero upon reaching the reference mark (see also
                SA_SetPosition_S)

        Example:
            // move to reference mark and set to zero
            result = SA_FindReferenceMark_S(mcsHandle,0,SA_FORWARD_DIRECTION,0,SA_AUTO_ZERO);
            unsigned int status;
            do {
                SA_GetStatus_S(mcsHandle,0,&status);
            } while (status != SA_STOPPED_STATUS);

        """

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

    def GetAngleLimit_S(self):
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

        ret = self.dll.SA_GetClosedLoopMoveSpeed_S(c_systemIndex, c_channelIndex, byref(c_speed))
        return (ret, c_speed)

    def GetEndEffectorType_S(self):
        pass

    def GetForce_S(self):
        pass

    def GetGripperOpening_S(self):
        pass

    def GetPhysicalPositionKnown_S(self, systemIndex, channelIndex):

        """
        Channel type: Positioner

        Interface:
        SA_STATUS SA_GetPhysicalPositionKnown_S(SA_INDEX systemIndex,
                                                SA_INDEX channelIndex,
                                                unsigned int *known);

        Description:
        Returns whether the positioner “knows” its physical position. After a power-up the physical position is unknown
        and the current position is implicitly assumed to be the zero position. After the reference mark has been found
        by calling SA_FindReferenceMark_S the physical position becomes known.

        This function can be useful if the software application restarts and connects to a system that has stayed
        online. If the physical position is already known, traveling to the reference mark again may be omitted.

        See also 2.5.3 “Defining Positions“.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is
                zero based.
            :return known: (unsigned 32bit), output - If the call was successful, this parameter will be either
                SA_PHYSICAL_POSITION_UNKNOWN (0) or SA_PHYSICAL_POSITION_KNOWN (1).

            Example:
            // check whether the physical position of channel 2 is known
            unsigned int known;
            result = SA_GetPhysicalPositionKnown_S(mcsHandle,2,&known);
            if (result == SA_OK) {
                // known holds the result
            }

            See also:SA_FindReferenceMark_S, SA_SetPosition_S, SA_SetScale_S
        """

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_known = c_uint32()

        ret = self.dll.SA_GetPhysicalPositionKnown_S(c_systemIndex, c_channelIndex, byref(c_known))
        return (ret, c_known.value)

    def GetPosition_S(self, systemIndex, channelIndex):

        """
        Channel type: Positioner

        Interface:SA_STATUS SA_GetPosition_S(SA_INDEX systemIndex,
                                             SA_INDEX channelIndex,
                                             signed int *position);

        Description:
        Returns the current position of a positioner. This function is only executable by a positioner that has a sensor
        attached to it. The sensor must also be enabled or in power save mode (see SA_SetSensorEnabled_S). If this is
        not the case the channel will return an error. Additionally, the command is only executable if the addressed
        channel is configured to be of type linear (see SA_SetSensorType_S). A rotary channel will return an error
        (use SA_GetAngle_S instead).

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is
                zero based.
            :return position :(signed 32bit), output - If the call was successful this value holds the current position
                of the positioner in nano meters.

        Example:
        unsigned int mcsHandle;
        const char loc[] = “usb:id:3118167233”;
        SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
        if (result != SA_OK) {
            // handle error...
        }
        // get current position
        signed int position;
        result = SA_GetPosition_S(mcsHandle,0,&position);
        if (result == SA_OK) {
            // current position is in position variable
        }

        See also:SA_GetAngle_S
        """

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_position = c_int32()

        ret = self.dll.SA_GetPosition_S(c_systemIndex, c_channelIndex, byref(c_position))
        return (ret, c_position.value)

    def GetPositionLimit_S(self, systemIndex, channelIndex):

        """
        Description:
        Inverse function to SA_SetPositionLimit_S. May be used to read out the travel range limit that is currently
        configured for a linear channel.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is
                zero based.
            :return minPosition: (signed 32bit), output - If the call was successful, this parameter holds the absolute
                minimum position given in nanometers.
            :return maxPosition: (signed 32bit), output - If the call was successful, this parameter holds the absolute
                maximum position given in nanometers.
        Note: If no limit is set then both minPosition and maxPosition will be 0.


        """


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

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_scale = c_int32()
        c_inverted = c_uint32()

        ret = self.dll.SA_GetScale_S(c_systemIndex, c_channelIndex, byref(c_scale), byref(c_inverted))
        return (ret, c_scale.value, c_inverted.value)

        pass

    def GetSensorEnabled_S(self, systemIndex):
        """
        Interface:
        SA_STATUS SA_GetSensorEnabled_S(SA_INDEX systemIndex,
                                        unsigned int *enabled);

        Description:
        This function may be used to read the sensor operation mode that is currently configured for the sensors that
        are attached to the positioners of a system. The mode is system global and applies to all positioner channels
        of a system equally.

        Please refer to section 2.5.2 “Sensor Modes” for more information on the sensor modes.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :returns enabled: (unsigned 32bit), output - If the call was successful, this parameter holds the current
            sensor mode (SA_SENSOR_DISABLED (0), SA_SENSOR_ENABLED(1) or SA_SENSOR_POWERSAVE(2)).

        Example:
            unsigned int mcsHandle;
            const char loc[] = “usb:id:3118167233”;
            SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
            if (result != SA_OK) {
                // handle error...
            }
            // read sensor mode
            unsigned int enabled;
            result = SA_GetSensorEnabled_S(mcsHandle,&enabled);

            See also:SA_SetSensorEnabled_
        """

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

        """
        Channel type: Positioner

        Interface:
        SA_STATUS SA_GotoPositionRelative_S(SA_INDEX systemIndex,
                                            SA_INDEX channelIndex,
                                            signed int diff,
                                            unsigned int holdTime);

        Description:
        Instructs a positioner to move to a position relative to its current position. This function is only executable
        by a positioner that has a sensor attached to it. The sensor must also be enabled or in power save mode
        (seeSA_SetSensorEnabled_S). If this is not the case the channel will return an error. Additionally, the command
        is only executable if the addressed channel is configured to be of type linear (seeSA_SetSensorType_S). A rotary
         channel will return an error (use SA_GotoAngleRelative_S instead).

        If a relative positioning command is issued before a previous one has finished, normally the relative targets
        are accumulated. If this is not desired it can be disabled with SA_SetAccumulateRelativePositions_S(see there
        for more information).

        The positioner may be instructed to hold the target position after it has been reached. See
        SA_GotoPositionAbsolute_S for more information.

        While executing the command the positioner will have a movement status of SA_TARGET_STATUS. While holding the
        target position the positioner will have a movement status of SA_HOLDING_STATUS (seeSA_GetStatus_S).

        If a mechanical end stop is detected while the command is in execution, the movement will be aborted. Note that
        in asynchronous communication mode an error will be reported.

        Parameters:
        :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
        :param channelIndex: (unsigned 32bit), input - Selects the channel of the selected system. The index is zero
            based.
        :param position: (signed 32bit), input - Relative position to move to in nano meters.
        :param holdTime: (unsigned 32bit), input - Specifies how long (in milliseconds) the position is actively held
        after reaching the target. The valid range is 0..60,000. A 0 deactivates this feature, a value of 60,000 is
        infinite (until manually stopped, see SA_Stop_S).

        Example:
            // move 2 micro meters in negative direction
            result = SA_GotoPositionRelative_S(mcsHandle,0,-2000,0);

        See also:SA_GotoPositionAbsolute_S, SA_GotoAngleRelative_S, SA_GetPosition_S
        """

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_diff = c_int32(diff)
        c_holdTime = c_uint32(holdTime)

        ret = self.dll.SA_GotoPositionRelative_S(c_systemIndex, c_channelIndex, c_diff, c_holdTime)
        return (ret)

    def ScanMoveAbsolute_S(self, systemIndex, channelIndex, target, scanSpeed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_target = c_uint32(target)
        c_scanSpeed = c_uint32(scanSpeed)

        ret = self.dll.SA_ScanMoveAbsolute_S(c_systemIndex, c_channelIndex, c_target, c_scanSpeed)
        return (ret)

    def ScanMoveRelative_S(self, systemIndex, channelIndex, diff, scanSpeed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_diff = c_uint32(diff)
        c_scanSpeed = c_uint32(scanSpeed)

        ret = self.dll.SA_ScanMoveRelative_S(c_systemIndex, c_channelIndex, c_diff, c_scanSpeed)
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

        ret = self.dll.SA_SetChannelProperty_S(c_systemIndex, c_channelIndex, c_key, c_value)
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

        ret = self.dll.SA_SetClosedLoopMoveAcceleration_S(c_systemIndex, c_channelIndex, c_acceleration)
        return(ret)

    def SetClosedLoopMoveSpeed_S(self, systemIndex, channelIndex, speed):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_speed = c_uint32(speed)

        ret = self.dll.SA_SetClosedLoopMoveSpeed_S(c_systemIndex, c_channelIndex, c_speed)
        return (ret)

    def SetEndEffectorType_S(self):
        pass

    def SetPosition_S(self, systemIndex, channelIndex, position):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_position = c_int32(position)

        ret = self.dll.SA_SetPosition_S(c_systemIndex, c_channelIndex, c_position)
        return (ret)

    def SetPositionLimit_S(self, systemIndex, channelIndex, minPosition, maxPosition):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_minPosition = c_int32(minPosition)
        c_maxPosition = c_int32(maxPosition)

        ret = self.dll.SA_SetPositionLimit_S(c_systemIndex, c_channelIndex, c_minPosition, c_maxPosition)
        return (ret)

    def SetSafeDirection_S(self, systemIndex, channelIndex, direction):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_direction = c_uint32(direction)

        ret = self.dll.SA_SetSafeDirection_S(c_systemIndex, c_channelIndex, c_direction)
        return (ret)

    def SetScale_S(self, systemIndex, channelIndex, scale, inverted):

        c_systemIndex = c_uint32(systemIndex)
        c_channelIndex = c_uint32(channelIndex)
        c_scale = c_int32(scale)
        c_inverted = c_uint32(inverted)

        ret = self.dll.SA_SetScale_S(c_systemIndex, c_channelIndex, c_scale, c_inverted)
        return (ret)

    def SetSensorEnabled_S(self, systemIndex, enabled):

        """
        Interface:
            SA_STATUS SA_SetSensorEnabled_S(SA_INDEX systemIndex,
                                            unsigned int enabled);

        Description:
        This function may be used to activate or deactivate the sensors that are attached to the positioners of a
        system. The command is system global and affects all positioner channels of a system equally. It effectively
        turns the power supply of the sensors on or off. Please refer to section 2.5.2 “Sensor Modes” for more
        information on the sensor modes. End effector channels are not affected by this function.

        If this command is issued, all positioner channels of the system are implicitly stopped.

        This setting is stored to non-volatile memory immediately and need not be configured on every power-up.

        Parameters:
            :param systemIndex: (unsigned 32bit), input - Handle to an initialized system.
            :param enabled: (unsigned 32bit), input - Sets the mode. Must be either SA_SENSOR_DISABLED (0),
                SA_SENSOR_ENABLED (1) or SA_SENSOR_POWERSAVE (2).
        Example:
            unsigned int mcsHandle;
            const char loc[] = “usb:id:3118167233”;
            SA_STATUS result = SA_OpenSystem(&mcsHandle, loc, “sync”);
            if (result != SA_OK) {
                // handle error...
            }
            // disable sensors
            result = SA_SetSensorEnabled_S(mcsHandle,SA_SENSOR_DISABLED);

        See also:SA_GetSensorEnabled_S
        """

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

        ret = self.dll.SA_StepMove_S(c_systemIndex, c_channelIndex, c_steps, c_frequency, c_amplitude)
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









