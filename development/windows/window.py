class Window:
    '''Родительский класс окон'''

    def __init__(self, screen, size, main):
        '''Инициализация класа'''
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.one_size = self.main_screen.board.cell_size

    def parse_text(self, text, width):
        '''Функция парсинга текста'''
        lst = text.split()
        res = []
        w = width
        st = ''
        while len(lst) > 1:
            while w > 0 and len(lst) > 1:
                if len(lst[0]) > 0:
                    st += lst[0] + ' '
                    lst = lst[1:]
                    w -= len(lst[0])
                else:
                    break
            w = width
            res.append(st)
            st = ''
        return res
