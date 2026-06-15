# pylint: skip-file
import utilities as ut

#########################################################################################
#
# Variables
#
#########################################################################################
# Verbosity, dirty_anual_wage
verbose, dirty_anual_wage = ut.parse_arguments()

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

# Tramos IRPF para el estado español (2026)
app_irpf_sp = {
    "tramo_1": {"min": 0, "max": 12450, "irpf": 0.095},
    "tramo_2": {"min": 12450, "max": 20200, "irpf": 0.12},
    "tramo_3": {"min": 20200, "max": 35200, "irpf": 0.15},
    "tramo_4": {"min": 35200, "max": 60000, "irpf": 0.185},
    "tramo_5": {"min": 60000, "max": 300000, "irpf": 0.225},
    "tramo_6": {"min": 300000, "max": float("inf"), "irpf": 0.245},
}

# Tramos IRPF para la comunidad autónoma Catalunya (2026)
app_irpf_cat = {
    "tramo_1": {"min": 0,       "max": 12450,       "irpf": 0.105},
    "tramo_2": {"min": 12450,   "max": 17707,       "irpf": 0.12},
    "tramo_3": {"min": 17707,   "max": 21000,       "irpf": 0.14},
    "tramo_4": {"min": 21000,   "max": 33007,       "irpf": 0.15},
    "tramo_5": {"min": 33007,   "max": 53407,       "irpf": 0.188},
    "tramo_6": {"min": 53407,   "max": 90000,       "irpf": 0.215},
    "tramo_7": {"min": 90000,   "max": 120000,      "irpf": 0.235},
    "tramo_8": {"min": 120000,  "max": 175000,      "irpf": 0.245},
    "tramo_9": {"min": 175000,  "max": float("inf"),"irpf": 0.255},
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
def calc_irpf(base, tramos, verbose):
    money_to_pay = 0

    for tramo_name, tramo in tramos.items():
        tramo_money = 0

        if base > tramo["min"]:
            if base > tramo["max"]:
                tramo_money = (tramo["max"] - tramo["min"]) * tramo["irpf"]
            else:
                tramo_money = (base - tramo["min"]) * tramo["irpf"]
            
            money_to_pay += tramo_money 

            if verbose:
                print("---")
                print(f"{tramo_name}: {tramo}")
                print(f"> Money to pay in this tramo: {tramo_money:,.2f} €".replace(",", " "))
                print(f"> Accumulated money to pay: {money_to_pay:,.2f} €".replace(",", " "))
    
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
irpf_sp = calc_irpf(base_imponible, app_irpf_sp, verbose)

# Calcular IRPF Autonómico
print("\nCalculando IRPF Autonómico...")
irpf_cat = calc_irpf(base_imponible, app_irpf_cat, verbose)

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
