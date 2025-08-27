
# SIA TP1 - Métodos de Búsqueda

Se desarrolló un motor de búsqueda que resuelve un tablero siguiendo las reglas del juego **Sokoban**.  
El sistema permite variar los métodos de búsqueda empleados y las heurísticas definidas, otorgando mayor personalización y la posibilidad de observar los diferentes costos computacionales.

### Prerrequisitos
- [Python](https://www.python.org/downloads/) instalado en el sistema.
- `pip` disponible en la terminal (`pip --version` para verificar).

## Construcción:

Para construir el proyecto por completo y contar con el entorno necesario, ejecute de manera secuencial los siguientes comandos desde la raiz:

### Windows:

    python -m venv venv

    .\venv\Scripts\activate

    pip install -r requirements.txt

### Linux/MacOS

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    

## Ejecución

Para correr un programa, ejecute:
### Windows:

    python main.py <board_file_path> <algorithm>

### Linux/MacOS:

    python3 main.py <board_file_path> <algorithm>

Donde `<algorithm>` puede ser una de las siguientes opciones:

- `bfs` — Breadth-First Search
- `dfs` — Depth-First Search
- `iddfs` — Iterative Deepening DFS
- `greedy` — Búsqueda Greedy Best-First
- `astar` — Algoritmo A*


## Testing

Para correr un programa que ejecute la combinación de todos los algoritmos y heurísticas en los tableros, ejecute desde la raíz:

### Windows:

    python run_experiments.py boards/b1.txt

### Linux/MacOS:

    python3 run_experiments.py boards/b1.txt
    
También es posible pasar más de un tablero como argumento, por ejemplo:

    python run_experiments.py boards/b2.txt boards/b7.txt boards/b1.txt

### Archivos de salida

Al ejecutar `run_experiments.py` los resultados generados por el testing se guardan en una carpeta llamada `Results`.  
Cada tablero produce un archivo CSV con el nombre `<board>_results.csv`.  

Por ejemplo, el archivo `b1_results.csv` contendrá un header con las siguientes columnas:

    board,algorithm,heuristic,result,cost,expanded,frontier,duration_sec

- **board**: nombre del tablero utilizado
- **algorithm**: algoritmo de búsqueda empleado
- **heuristic**: heurística aplicada (si corresponde)
- **result**: indica si se encontró una solución o no
- **cost**: costo de la solución encontrada
- **expanded**: cantidad de nodos expandidos
- **frontier**: cantidad de nodos en la frontera al finalizar
- **duration_sec**: tiempo de ejecución en segundo

---

## Autores:

| Nombre | Legajo |
| ------ | ------ |
| BADIN, DIEGO | 63551 |
| RABINOVICH, DIEGO | 63155 |
| VALENTINA MARTI, RETA | 63225 |
| MARIANO IVAN, ODZOMEK | 63386
| JULIETA, TECHENSKI | 62547 |



