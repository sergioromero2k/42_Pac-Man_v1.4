## El proyecto
---
Estáis haciendo el **Pac-Man** de 42 Madrid, en Python, entre 2 personas. 
* Tú eres Persona A (Core/Lógica de juego)
* Tu compañero es Persona B (UI/Renderizado).

El subject exige; juego completo con menú, configuración por JSON, highscore persistente, cheat mode, generador de laberintos externo (no propio), y despliegue en `Itch.io/Steam.`

### La arquitectura general (de arriba a abajo)
```
GameEngine (orquesta menú/pausa/partida/game over) — 0..1 activo
    ├── Config / ConfigLoader (parámetros leídos del JSON)
    ├── CheatManager (trucos activos: invencibilidad, fantasmas congelados, velocidad)
    ├── HighscoreManager (ranking persistente)
    ├── Player (creado UNA vez, sobrevive entre niveles — vidas y puntuación)
    └── GameState (se crea y destruye en cada nivel)
            ├── Player ◇ (agregación — el mismo objeto de GameEngine, no una copia)
            ├── Ghost x4 ◆ (composición — nuevos en cada nivel)
            ├── Pacgum xN ◆ (composición — nuevas en cada nivel)
            └── Maze ◆ (composición — generado por MazeLoader en cada nivel)
``