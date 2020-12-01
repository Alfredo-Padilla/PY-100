import pygame
from itertools import chain

def truncline(text, font, maxwidth):
        #print('Truncline: ', text)
        real = len(text)       
        stext = text           
        l = font.size(text)[0]
        cut = 0
        a = 0                  
        done = 1
        old = None
        while l > maxwidth:
            a = a+1
            n = text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext = n[:-cut]
            else:
                stext = n
            l = font.size(stext)[0]
            real = len(stext)               
            done = 0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done = 0                      
    wrapped = []                  
                               
    while not done:             
        nl, done, stext = truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text = text[nl:]

    #print(wrapped)
    sal = []
    for i in wrapped:
        aux = i.split('\r')
        if aux != i:
            for j in aux:
                sal.append(j)
        else:
            sal.append(aux)

    #print(sal)                
    return sal


def wrap_multi_line(text, font, maxwidth):
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

def nombre_variable(var, locals):
    '''
    for k,v in globals().items():
        if v == var:
            print('Buena', k, v)
        print(k, v)
    '''
    return [k for k,v in locals.items() if v == var][0]

if __name__ == '__main__':
    pygame.init() 
    font = pygame.font.Font(None, 17)
    print( wrapline("Now is the time for all good men to come to the aid of their country", font, 120))