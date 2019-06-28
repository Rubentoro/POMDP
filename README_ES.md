# POMDP

##### [Read in English](README.md)

## Implementación y análisis de Procesos de Decisión Parcialmente Observables de Markov en Python.

Este proyecto se ha realizado con propósitos educativos para 
la asignatura 'Inteligencia Artificial' del grado Ingeniería Informática de Software de la Universidad de Sevilla.

El objetivo del proyecto es estudiar y dar solución a un problema de decisión estableciendo probabilidades de tomar ciertas decisiones y estableciendo recompensas según la situación actual, la acción tomada y su consecuencia final (es decir, una función de transición T(s, a, s')).

Un problema POMDP se resuelve encontrando el criterio de acciones a seguir de forma que se maximice la recompensa final.

Utilizamos la librería [PyPOMDP](https://github.com/namoshizun/PyPOMDP).

Más información sobre POMDP disponible en [pomdp.org](http://www.pomdp.org/)


## Estructura del código fuente

El código fuente implementado, además de la citada librería, se divide en tres ficheros .py, los cuales se detallan a continuación en orden de ejecución:

* [gui.py](pomdp/gui.py): La interfaz gráfica de la aplicación, realizada usando [TkInter](https://wiki.python.org/moin/TkInter). Proporciona la opción de ejecutar la simulación de los problemas disponibles en sus diferentes modos de ejecución (interactivo, silencioso y benchmark), estos modos de ejecución se detallarán más adelante. Ofrece la posibilidad de visualizar la salida de la ejecución tanto en la propia interfaz como en la terminal del sistema operativo. Las llamadas que realiza la interfaz tienen como destino las funciones disponibles en el archivo app.py

* [app.py](pomdp/app.py): Tiene como función hacer las llamadas a la librería para leer los ficheros '.pomdp' (ficheros donde se definen los problemas a resolver) y hacer las llamadas a los métodos del archivo 'runner.py' que utilizan métodos de la librería para dar una solución completa al problema. Los datos necesarios para llamar a los diferentes métodos 'run' diseñados específicamente para cada problema son: `env` (archivo .pomdp a resolver), `config` (algoritmo para resolver el problema: pomcp o pbvi), `budget` (presupuesto para resolver el problema, se utiliza para asumir el coste de las diferentes acciones) y `max_play` (número máximo de iteraciones a realizar, 0 para desactivar este límite).

* [runner.py](pomdp/runner.py): Crea el modelo y el resolvedor (que empaqueta el algoritmo utilizado) y realiza las llamadas a la librería necesaria para obtener soluciones y calcular estadísticas. Contiene un método definido para cada problema disponible en cada uno de los tres modos de ejecución (interactivo, silencioso y benchmark).


## Demo

### Modo interactivo
Se ejecuta la simulación mostrándose las iteraciones paso a paso.

![Interactive mode](.github/demo/demo-interactive.gif)

### Modo silencioso
Se ejecuta la simulación hasta un estado de parada y se muestra el número de
pasos y la recompensa acumulada.

![Interactive mode](.github/demo/demo-silent.gif)

### Modo benchmark
Se ejecuta 30 veces el modo silencioso y al final se muestran estadísticas,
concretamente la media y la desviación típica del número de pasos y la recompensa
acumulada.
![Benchmark mode](.github/demo/demo-benchmark.gif)


## Realización de experimentos

Basta con introducir en la interfaz, los valores que queramos para cada problema definido y el algoritmo a utilizar.


## Reproducción de experimentos realizados

Los resultados de cada experimento son aleatorios en cada iteración por la naturaleza del problema que tratamos (resolución de problemas con incertidumbre o pomdp). Por este motivo, puede que se de el caso de no llegar a una solución final debido a no conseguir la condición de parada, superar el número máximo de iteraciones o gastar el budget por completo.

### Experimento \#1
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#2
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#3
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#4
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#5
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#6
- Select the problem to solve: `tiger`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#7
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#8
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#9
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#10
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `10`
- Mode: `interactive`

### Experimento \#11
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `10`
- Mode: `silent`

### Experimento \#12
- Select the problem to solve: `tag`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#13
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#14
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#15
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#16
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `10`
- Mode: `interactive`

### Experimento \#17
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `10`
- Mode: `silent`

### Experimento \#18
- Select the problem to solve: `bridge`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#19
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#20
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#21
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pomcp`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`

### Experimento \#22
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `interactive`

### Experimento \#23
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `silent`

### Experimento \#24
- Select the problem to solve: `car`
- Select the algorithm to solve the problem: `pbvi`
- Budget: `100`
- Maximum play times: `0`
- Mode: `benchmark`