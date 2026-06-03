Simulador de Chispazo educativo

Proyecto de práctica de **Python** que simula el juego de lotería mexicano *Chispazo*.
Eliges 5 números del 1 al 28, la urna sortea 5 al azar y ganas un premio según
cuántos números aciertes.

Este proyecto demuestra cómo aplicar conceptos de **programación lógica y de azar**
en un programa real y funcional.

¿Qué hace el programa?

1. **Jugar una partida** — eliges tus números (o usas una jugada automática rápida al azar) y compites contra el sorteo.
2. **Simular muchos sorteos** — repite miles de sorteos y compara las probabilidades reales contra las teóricas.
3. **Ver estadísticas** — guarda tu historial de partidas en un archivo y muestra tu balance de combinaciones jugadas acumulado.


¿Qué demuestra este proyecto? 

| Concepto de Python | Dónde se usa |
|---|---|
| Módulo `random` | Generar jugadas y sorteos al azar |
| Listas y conjuntos (`set`) | Comparar números y contar aciertos |
| Diccionarios | Guardar las estadísticas del jugador |
| Lectura/escritura de archivos (`json`) | Guardar el historial entre sesiones |
| `collections.Counter` | Contar frecuencias en la simulación |
| Combinatoria (`math.comb`) | Calcular probabilidades teóricas |
| Funciones, ciclos y validación de datos | Toda la estructura del programa |

---

La parte matemática 

El total de combinaciones posibles es **C(28, 5) = 98,280**.
La probabilidad de acertar los 5 números es de **1 entre 98,280**.

El modo de simulación demuestra la **Ley de los Grandes Números**. Mientras más
sorteos simulas, más se parecen los resultados reales a la probabilidad teórica.
Esto nos confirma que el sorteo es justo y completamente aleatorio. Ya que, no hay patrones
que permitan predecir los resultados.

Ejemplo de salida con 200,000 sorteos simulados:

```
Aciertos |      Veces |    Real % |  Teorica %
------------------------------------------------
       5 |          3 |   0.0015% |    0.0010%
       4 |        234 |   0.1170% |    0.1170%
       3 |      5,121 |   2.5605% |    2.5743%
       2 |     36,235 |  18.1175% |   18.0199%
       1 |     89,773 |  44.8865% |   45.0499%
       0 |     68,634 |  34.3170% |   34.2379%
```


## ▶️ Cómo ejecutarlo

No necesitas instalar nada, solo usa Python 3 (incluido en GitHub Codespaces).

```bash
python3 simulador_chispazo.py
```

---

Posdata

Este es un **simulador con fines de aprendizaje**. No es una herramienta para ganar
dinero: las probabilidades muestran justamente lo contrario. El objetivo es practicar
programación, lógica y estadística de forma divertida.
