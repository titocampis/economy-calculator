# pylint: skip-file
# https://atc.gencat.cat/es/tributs/irpf/
# https://taxdown.es/irpf/tabla-tramos/
import utilities as ut

#########################################################################################
#
# Variables
#
#########################################################################################
# Salario bruto anual
dirty_anual_wage = 52174.44

# Si True, se calcula el porcentaje sobre la base imponible, IRPF que descuenta empresa
# Si False, se calcula sobre el salario bruto, IRPF total que te chuclan.
perc_sobre_base = False  

#########################################################################################
#
# / Variables
#
#########################################################################################

#########################################################################################
#
# Constants
#
#########################################################################################
# Porcentaje seguridad social (va cambiando anualmente)
PER_SS = 0.0647 # Contingencias comunes, desempleo y formación profesional

# Tramos IRPF para el estado español (2025)
app_irpf_sp = {
    "tramo_1": {"min": 0, "max": 12500, "irpf": 0.095}, # min 0
    "tramo_2": {"min": 12500, "max": 22000, "irpf": 0.125}, # min 1187.5
    "tramo_3": {"min": 22000, "max": 33000, "irpf": 0.16}, # min 1187.5 + 1187 = 2374.5
    "tramo_4": {"min": 33000, "max": 53000, "irpf": 0.19}, # min 1187.5 + 1187 + 1760 = 4135
    "tramo_5": {"min": 53000, "max": 90000, "irpf": 0.215}, # min 1187.5 + 1187 + 1760 + 3800 = 7935
    "tramo_6": {"min": 90000, "max": 120000, "irpf": 0.235}, # min 1187.5 + 1187 + 1760 + 3800 + 8050 = 15985
    "tramo_7": {"min": 120000, "max": 175000, "irpf": 0.245}, # min 1187.5 + 1187 + 1760 + 3800 + 8050 + 7050 = 22940
    "tramo_8": {"min": 175000, "max": float("inf"), "irpf": 0.255}, # min 1187.5 + 1187 + 1760 + 3800 + 8050 + 7050 + 13475 = 36415
}

# Tramos IRPF para la comunidad autónoma Catalunya (2025)
app_irpf_cat = {
    "tramo_1": {"min": 0, "max": 6000, "irpf": 0.095}, # min 0
    "tramo_2": {"min": 6000, "max": 50000, "irpf": 0.105}, # min 570
    "tramo_3": {"min": 50000, "max": 200000, "irpf": 0.115}, # min 570 + 4620 = 5190
    "tramo_4": {"min": 200000, "max": 300000, "irpf": 0.135}, # min 570 + 4620 + 17250 = 22440
    "tramo_5": {"min": 300000, "max": float("inf"), "irpf": 0.14}, # min 570 + 4620 + 17250 + 13500 = 35940
}

#########################################################################################
#
# / Constants
#
#########################################################################################

#########################################################################################
#
# Methods
#
#########################################################################################
def calc_irpf(base, tramos):
    money_to_pay = 0

    for tramo_name, tramo in tramos.items():
        if base > tramo["min"]:
            if base > tramo["max"]:
                money_to_pay += (tramo["max"] - tramo["min"]) * tramo["irpf"]
            else:
                money_to_pay += (base - tramo["min"]) * tramo["irpf"]
        
            print(f"{tramo_name}: {tramo}")
            print(f"> Money to pay: {money_to_pay:,.2f} €".replace(",", " "))
    
    return money_to_pay

#########################################################################################
#
# / Methods
#
#########################################################################################

#########################################################################################
#
# Main
#
#########################################################################################
# Calculate base imponible anual = salario - cuotas seguridad social
ss = dirty_anual_wage * PER_SS
base_imponible = dirty_anual_wage - ss
print(f"---\nBase Imponible: {ut.format_es(base_imponible)} €\n---")

# Calcular IRPF Estatal
print("\nCalculando IRPF Estatal...")
irpf_sp = calc_irpf(base_imponible, app_irpf_sp)

# Calcular IRPF Autonómico
print("\nCalculando IRPF Autonómico...")
irpf_cat = calc_irpf(base_imponible, app_irpf_cat)

# Total IRPF
irpf_total = irpf_sp + irpf_cat

# Salario neto
salario_neto = base_imponible - irpf_total

if perc_sobre_base:
    print(
        "\n*********************************************************************\n"
        f"Salario Bruto anual               = {ut.format_es(dirty_anual_wage, 0)} €\n"
        f"Salario Bruto mensual (12 pagas)  = {ut.format_es(dirty_anual_wage/12)} €\n---\n"
        f"Cuotas SS anual                   = {ut.format_es(ss)} € "
        f"({100 * PER_SS:,.2f} %)\n"
        f"Deducción IRPF Estatal anual      = {ut.format_es(irpf_sp)} € ({(100 * irpf_sp / base_imponible):,.2f} %)\n"
        f"Deducción IRPF Autonómica anual   = {ut.format_es(irpf_cat)} € ({(100 * irpf_cat / base_imponible):,.2f} %)\n---\n"
        f"Deducción Total IRPF anual        = {ut.format_es(irpf_total)} € "
        f"({(100 * irpf_total / base_imponible):,.2f} %)\n"
        f"Deducción Total IRPF + SS         = {ut.format_es(irpf_total + ss)} € \n---\n"
        f"Salario Neto anual                = {ut.format_es(salario_neto)} €\n"
        f"Salario Neto mensual  (12 pagas)  = {ut.format_es(salario_neto/12)} €\n"
        "*********************************************************************\n"
    )

else:
    print(
        "\n*********************************************************************\n"
        f"Salario Bruto anual               = {ut.format_es(dirty_anual_wage, 0)} €\n"
        f"Salario Bruto mensual (12 pagas)  = {ut.format_es(dirty_anual_wage/12)} €\n---\n"
        f"Cuotas SS anual                   = {ut.format_es(ss)} € "
        f"({100 * PER_SS:,.2f} %)\n"
        f"Deducción IRPF Estatal anual      = {ut.format_es(irpf_sp)} € ({(100 * irpf_sp / dirty_anual_wage):,.2f} %)\n"
        f"Deducción IRPF Autonómica anual   = {ut.format_es(irpf_cat)} € ({(100 * irpf_cat / dirty_anual_wage):,.2f} %)\n---\n"
        f"Deducción Total IRPF anual        = {ut.format_es(irpf_total)} € "
        f"({(100 * irpf_total / dirty_anual_wage):,.2f} %)\n"
        f"Deducción Total IRPF + SS         = {ut.format_es(irpf_total + ss)} € "
        f"({(100 * (irpf_total + ss) / dirty_anual_wage):,.2f} %)\n---\n"
        f"Salario Neto anual                = {ut.format_es(salario_neto)} €\n"
        f"Salario Neto mensual  (12 pagas)  = {ut.format_es(salario_neto/12)} €\n"
        "*********************************************************************\n"
    )

#########################################################################################
#
# / Main
#
#########################################################################################