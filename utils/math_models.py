# utils/math_models.py
import math

def calcular_r_exponencial(p0, p1, t):
    """
    Calcula la tasa de crecimiento (r) para el modelo exponencial (Malthus).
    r = ln(P1 / P0) / t
    """
    if p0 <= 0 or p1 <= 0 or t <= 0:
        return 0.0
    return math.log(p1 / p0) / t

def calcular_r_logistico(p0, p1, t, k):
    """
    Calcula la tasa de crecimiento (r) para el modelo Logístico (Verhulst).
    r = (1/t) * ln( [P1 * (K - P0)] / [P0 * (K - P1)] )
    """
    if p0 <= 0 or p1 <= 0 or t <= 0 or k <= p0 or k <= p1:
        return 0.0
    
    numerador = p1 * (k - p0)
    denominador = p0 * (k - p1)
    
    # Prevenir errores de dominio en el logaritmo
    if numerador / denominador <= 0:
        return 0.0
        
    return math.log(numerador / denominador) / t

def simular_exponencial(p0, r, t_total):
    """
    Genera la lista de poblaciones año por año usando P(t) = P0 * e^(rt)
    """
    return [p0 * math.exp(r * t) for t in range(t_total + 1)]

def simular_logistico(p0, r, k, t_total):
    """
    Genera la lista de poblaciones año por año usando P(t) = K / (1 + C * e^(-rt))
    """
    if p0 <= 0:
        return [0] * (t_total + 1)
        
    c = (k - p0) / p0
    poblaciones = []
    
    for t in range(t_total + 1):
        try:
            p = k / (1 + c * math.exp(-r * t))
        except OverflowError:
            p = k  # Si el exponente es muy grande, se asume que llegó al límite K
        poblaciones.append(p)
        
    return poblaciones