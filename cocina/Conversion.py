from django.core.exceptions import ValidationError

def calculadora_unitario(medida_compra,medida_uso,costo,cantidad):

    if costo > 0:

        # Primer caso si las unidades son iguales
        if medida_compra == medida_uso:
            costo_unitario = costo * cantidad
            return costo_unitario

        # Segundo caso si es unidades, solo se puede usar unidades
        elif medida_compra == "Unidades":

            if medida_uso != "Unidades":
                raise ValidationError("La unica medida de uso aceptada es 'Unidades'.")     

        # Tercer caso si es Kilogramos, solo se puede usar Kilogramos o gramos.
        elif medida_compra == "Kilogramos":

            if medida_uso == "Gramos":
                costo_unitario = ( costo  / 1000 ) * cantidad
                return costo_unitario
            
            else:
                raise ValidationError("El producto comprado tiene unidad de medida 'Kilogramos', por lo que sólo puede seleccionar 'Kilogramos' o 'Gramos' como medida de uso.") 

        # Cuerto caso si es litros, solo se puede usar litros o Mililitros.
        elif medida_compra == "Litros":

            if medida_uso == "Mililitros":
                costo_unitario = ( costo  / 1000 ) * cantidad
                return costo_unitario
            
            else:
                raise ValidationError("El producto comprado tiene unidad de medida 'Litros', por lo que sólo puede seleccionar 'Litros' o 'Mililitros' como medida de uso.") 

        # Quinto caso si es Gramos, solo se puede usar Gramos o Kilogramos.
        elif medida_compra == "Gramos":

            if medida_uso == "Kilogramos":
                costo_unitario = costo * cantidad * 1000
                return costo_unitario
            
            else:
                raise ValidationError("El producto comprado tiene unidad de medida 'Gramos', por lo que sólo puede seleccionar 'Gramos' o 'Kilogramos' como medida de uso.") 
        
        # Sexto caso si es Mililitros, solo se puede usar Mililitros o Litros.
        elif medida_compra == "Mililitros":

            if medida_uso == "Litros":
                costo_unitario = costo * cantidad * 1000
                return costo_unitario
            
            else:
                raise ValidationError("El producto comprado tiene unidad de medida 'Mililitros', por lo que sólo puede seleccionar 'Mililitros' o 'Litros' como medida de uso.") 

        # Sexto caso si es Mililitros, solo se puede usar Mililitros o Litros.
        elif medida_compra == "Libras":

            if medida_uso == "Onzas":
                costo_unitario = (costo / 16) * cantidad
                return costo_unitario
        
            else:
                raise ValidationError("El producto comprado tiene unidad de medida 'Libras', por lo que sólo puede seleccionar 'Libras' u 'Onzas' como medida de uso.") 

