singular = {
    ' miliardi ': ' miliardo ',
    ' milioni ': ' milione ',
}

def _italian_int(val, unit=None):
    if val<0:
        return ['meno'] + _italian_int(-val, unit)
    rval=[]
    billions = val // 1000000000
    millions = (val // 1000000) % 1000
    thousands = (val // 1000) % 1000
    hundreds = (val // 100) % 10
    tens = (val // 10) % 10
    units = (val) % 10
    if billions>0:
        rval += _italian_int(billions, ' miliardi ')
    if millions>0:
        rval += _italian_int(millions, ' milioni ')
    if thousands>0:
        rval += _italian_int(thousands, 'mila')
    if hundreds>0:
        rval += _italian_int(hundreds, 'cento')
    unit_to_string = [
        'zero','uno','due','tre','quattro','cinque','sei','sette','otto','nove'
    ]
    ten_to_string = [
        '?','?','venti','trenta','quaranta','cinquanta','sessanta','settanta','ottanta','novanta'
    ]
    if tens==1:
        teens_to_string = [
            'dieci','unidici','dodici','tredici','quattordici','quindici','sedici','diciassette','diciotto','diciannove'
        ]
        rval.append( teens_to_string[units] )
    else:
        if units==8 or units==1:
            rval.append(ten_to_string[tens][:-1]+unit_to_string[units])
        else:
            if tens>0:
                rval.append( ten_to_string[tens] )
            if units>0:
                rval.append( unit_to_string[units] )

            
    if unit=='mila' and val==1:
        rval.pop()
        rval.append( "mille" )
    elif unit=='cento' and val==1:
        rval.append( unit )
    elif unit is not None and val==1:
        rval.pop()
        rval.append( 'un' )
        rval.append( singular[unit] )
    else:
        if val==0:
            rval.append( "zero" )
        if unit is not None:
            rval.append( unit )
    return rval

def italian_int(val):
    return ''.join(_italian_int(val)).strip()


def test():
    print( italian_int(1985) )
    print( italian_int(11985) )
    print( italian_int(25000) )
    print( italian_int(25012) )
    print( italian_int(25024) )
    print( italian_int(25088) )
    print( italian_int(25003) )
    print( italian_int(1034008) )
    print( italian_int(4001034008) )
    print( italian_int(4034008) )
    print( italian_int(1001034008) )
    #for i in range(100):
    #    print( italian_int(i) )

if __name__ == "__main__":
    test()