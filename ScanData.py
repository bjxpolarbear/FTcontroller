

class DWdata():
    """docstring for DW1data"""

    def __init__(self, *argv):
        super(DWdata, self).__init__()

        self.input_parameter(*argv)

    def input_parameter(self, *argv):

        ### pass in the scan type ###
        try:
            self.type = argv[0]
        except:
            self.type = 'f'

        ### pass is the parameters ###
        try:
            self.para1 = argv[1]
        except:
            self.para1 = None
        try:
            self.para2 = argv[2]
        except:
            self.para2 = None
        try:
            self.para3 = argv[3]
        except:
            self.para3 = None


class SegmentData():
    """docstring for SegmentData"""

    def __init__(self, *argv):
        super(SegmentData, self).__init__()

        ### declare the size of the analog array and binary array ###
        ANALOG_SIZE = 36
        BINARY_SIZE = 32

        ### initialize the duration of the segment ###
        self.duration = 80

        ### initialize the digital waveform of the segment ###
        self.dw1data = DWdata(*argv)

        ### initialize the analog array of the segment ###
        self.analog_ini = [None] * ANALOG_SIZE
        self.analog_fin = [None] * ANALOG_SIZE

        ### initialize the binary array of the segment ###
        self.binary = [False] * BINARY_SIZE

    def __convert_none__(self, inp):
        # a not so elegent way to convert the None type to a 'N' for serial
        # talk ###
        if inp == None:
            return 'N'
        else:
            return str(inp)

    def __convert_bool__(self, inp):
        ### convert a bool type to 'T' or 'F' for serial talk ###
        if inp == True:
            return 'T'
        elif inp == False:
            return 'F'
        else:
            return -1

    def pack_segment_data(self):

        output = '<'

        ### adding in the duration data ###
        output += 'd ' + str(self.duration) + ' '

        ### adding in the digital waveform 1 data ###
        if str(self.dw1data.type) in {'r', 'm'}:
            output += str(self.dw1data.type) + ' '
            output += self.__convert_none__(self.dw1data.para1) + ' '
            output += self.__convert_none__(self.dw1data.para2) + ' '
            output += self.__convert_none__(self.dw1data.para3) + ' '
            output += 'a '
            for analog in self.analog_ini:
                output += self.__convert_none__(analog) + ' '
            for analog in self.analog_fin:
                output += self.__convert_none__(analog) + ' '

            ### adding in the binary data ###
            output += 'b '
            for binary in self.binary:
                output += self.__convert_bool__(binary) + ' '

            output += '> '
            print(output)
            return output

        if str(self.dw1data.type) in {'f'}:
            output += str(self.dw1data.type) + ' '    
            output += self.__convert_none__(self.dw1data.para1) + ' '
            output += self.__convert_none__(self.dw1data.para2) + ' '
            output += 'a '
            for analog in self.analog_ini:
                output += self.__convert_none__(analog) + ' '
            for analog in self.analog_fin:
                output += self.__convert_none__(analog) + ' '

            ### adding in the binary data ###
            output += 'b '
            for binary in self.binary:
                output += self.__convert_bool__(binary) + ' '

            output += '> '
            return output

        if str(self.dw1data.type) in {'c'}:
            output += str(self.dw1data.type) + ' '    
            output += self.__convert_none__(self.dw1data.para1) + ' '
            output += self.__convert_none__(self.dw1data.para2) + ' '
            output += self.__convert_none__(self.dw1data.para3)
            output += '> '
            return output

        if str(self.dw1data.type) in {'q'}:
            output += str(self.dw1data.type)
            output += '> '
            return output


class ScanData(list):  # inherient a list to this class ###
    """docstring for ScanData"""

    def __init__(self):
        super(ScanData, self).__init__()
        self.scan_string = ''
        self.segment_list = []

    def pack_scan_data(self):
        output_str = 'D '
        for segment in self.segment_list:
            output_str += segment.pack_segment_data()
        output_str += 'e'
        self.scan_string = output_str
        return output_str

    def to_gui(self):

        pass

    def from_gui(self):

        pass

    def save_file(self):
        
        pass

