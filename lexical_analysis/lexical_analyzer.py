from . import DFA

class Reader():
    def __init__(self, text=None):
        if isinstance(text, str):
            text = text + ' '
        self.text = text
        self.pointer = 0   # text pointer
        self.current_line = 1

    def sub_text(self, begin_pos, end_pos):
        return self.text[begin_pos: end_pos]

    def set_text(self, text):
        '''
        :param text: string
        '''
        self.text = text + ' '
        self.pointer = 0
        self.current_line = 1
        
    def set_text_from_file(self, path):
        with open(path) as f:
            self.set_text(f.read())

    def read_next(self):
        self.skip_annotation()
        return self.text[self.pointer]

    def is_EOF(self):
        '''return is EOF after skip_annotation'''
        self.skip_annotation()
        return self.EOF()

    def EOF(self):
        '''return is EOF before skip_annotation'''
        return self.pointer == len(self.text)

    def move_next(self):
        '''
        :return: False: EOF
        '''
        if self.text[self.pointer] == '\n':
            self.current_line += 1
        if self.pointer == len(self.text)-1:
            self.pointer += 1
            return False
        self.pointer += 1
        return True

    def skip_annotation(self):
        if self.pointer != len(self.text)-1:
            if self.text[self.pointer: self.pointer+2] == '//':
                self.move_next()
                self.move_next()
                while True:
                    if self.EOF():
                        break
                    elif self.text[self.pointer] == '\n':
                        self.move_next()
                        break
                    self.move_next()
                self.skip_annotation()
            elif self.text[self.pointer: self.pointer+2] == '/*':
                left_pos = self.current_line
                self.move_next()
                self.move_next()
                while True:
                    if self.pointer >= len(self.text)-1:
                        raise Exception('注释/*缺少右半边. (line:%d)'%(left_pos))
                    elif self.text[self.pointer: self.pointer+2] == '*/':
                        self.move_next()
                        self.move_next()
                        break
                    self.move_next()

class Lexical_Analyzer():
    def __init__(self, reader, dfa, vocab_table):
        self.reader = reader
        self.dfa = dfa
        self.vocab_table = vocab_table
        self.id_table = {}   # {str: count}
        self.int_const_table = {}   # {int: count}
        self.char_const_table = {}   # {str: count}
        self.float_const_table = {}

    def add_to_dict(self, item, d):
        if d.get(item, None) == None:
            d[item] = 1
        else:
            d[item] += 1

    def get_token(self):
        self.reader.skip_annotation()
        begin_pos = self.reader.pointer
        current_status = self.dfa
        while self.reader.is_EOF() == False:
            char = self.reader.read_next()
            if current_status.is_exist_next(char):
                current_status = current_status.next(char)
                self.reader.move_next()
            else:
                if current_status.is_acceptable():
                    accept_vocab = current_status.accept(self.vocab_table)
                    return self.make_token(accept_vocab, begin_pos, self.reader.pointer)
                else:
                    raise Exception('词法错误，字符不符合词法. (line:%d)'%self.reader.current_line)
        raise EOFError('EOF when getting token. (line%d)'% self.reader.current_line)

    def make_token(self, accept_vocab, begin_pos, end_pos):
        if accept_vocab == 'ws':
            return self.get_token()   # skip ws 空格和换行符，递归跳过
        elif accept_vocab == 'id':
            word = self.reader.sub_text(begin_pos, end_pos)
            self.add_to_dict(word, self.id_table)
            return ('id', word)
        elif accept_vocab == 'int_const':
            num = self.reader.sub_text(begin_pos, end_pos)
            num = int(num)
            self.add_to_dict(num, self.int_const_table)
            return ('int_const', num)
        elif accept_vocab == 'float_const':
            num = self.reader.sub_text(begin_pos, end_pos)
            num = float(num)
            self.add_to_dict(num, self.float_const_table)
            return ('float_const', num)   
        elif accept_vocab == 'char_const':
            char = self.reader.sub_text(begin_pos, end_pos)
            char = char[1]  # 'c' -> c
            self.add_to_dict(char, self.char_const_table)
            return ('char_const', char)
        elif accept_vocab in self.vocab_table:
            return (accept_vocab, None)
        else:
            raise Exception('Invalid accept vocab. 自动机支持的vocab，但是没有对应的token处理过程. (line:%d)'% self.reader.current_line)



