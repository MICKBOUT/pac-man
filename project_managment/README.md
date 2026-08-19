# Project Management

This document describes how the Pac-Man project was organised and developed.

## Team

| Login | Role |
|---------|---------|
| mboutte | Development, architecture, gameplay |
| mbichet | Development, testing, documentation |

Both team members participated in the design, implementation and review of the project.

---

# Development Method

The project was developed incrementally.

The objective was to first obtain a playable prototype and then progressively add all required features from the subject.

The work was divided into multiple milestones.

---

# Milestone 1 - Project Setup

## Goals

- Analyse the subject
- Create repository
- Configure development environment
- Configure dependencies
- Create initial architecture

## Deliverables

- Git repository
- Project structure
- Pygame initialisation
- Window creation
- Configuration loading

---

# Milestone 2 - Maze Integration

## Goals

- Integrate the provided mazegenerator package
- Create maze rendering
- Verify generated maps

## Deliverables

- Maze wrapper class
- Maze rendering system
- Seed management

---

# Milestone 3 - Player Movement

## Goals

- Implement Pac-Man entity
- Keyboard controls
- Collision with walls

## Deliverables

- Player movement
- Grid navigation
- Animation support

---

# Milestone 4 - Ghost System

## Goals

- Create ghost entities
- Implement pathfinding
- Implement different ghost behaviours

## Deliverables

- Ghost movement logic
- Target selection logic
- Pathfinding system

---

# Milestone 5 - Gameplay Features

## Goals

- Pac-Gums
- Super Pac-Gums
- Scoring system
- Lives system

## Deliverables

- Score management
- Vulnerable ghosts
- Level completion logic

---

# Milestone 6 - User Interface

## Goals

- Main menu
- Rules screen
- Pause menu
- Game over screen

## Deliverables

- Menu navigation
- Buttons
- Screen transitions

---

# Milestone 7 - Highscore System

## Goals

- Persistent highscores
- Player name registration
- Score sorting

## Deliverables

- JSON score storage
- Top 10 ranking
- Name input screen

---

# Milestone 8 - Validation and Error Handling

## Goals

- Validate configuration
- Handle invalid files
- Improve robustness

## Deliverables

- Pydantic validation
- User-friendly error messages
- Configuration constraints

---

# Milestone 9 - Packaging

## Goals

- Create distributable build
- Verify installation process

## Deliverables

- PyInstaller configuration
- Linux package
- Deployment archive

---

# Git Workflow

The project was developed using Git.

Main practices:

- Feature branches
- Pull requests / merge requests
- Merge commits
- Continuous integration of completed features

Examples:

- Initial architecture
- Maze integration
- Ghost implementation
- Highscore system
- Packaging and documentation

The complete development history can be reviewed through the Git commit log.

---

# Testing Strategy

Testing was performed continuously during development.

## Manual Testing

- Player movement
- Collision system
- Ghost behaviour
- Score system
- Menu navigation
- Highscore persistence

## Validation Testing

- Invalid configuration files
- Missing files
- Invalid values
- Empty highscore file

## Gameplay Testing

- Level progression
- Game over conditions
- Ghost vulnerability
- Score calculation

---

# Technical Decisions

## Pygame CE

Chosen because it provides a modern maintained version of Pygame suitable for graphical applications.

## Pydantic

Chosen for configuration validation and clear error reporting.

## JSON Highscores

Chosen because:

- Human readable
- Easy to edit
- No database required
- Portable

## Maze Generator Package

The subject explicitly provides a maze generation package.

The project wraps this package rather than reimplementing maze generation.

---

# Challenges Encountered

## Ghost Navigation

Finding reliable paths inside generated mazes required a dedicated pathfinding system.

## Separation of Logic and Rendering

The project was structured to keep gameplay logic independent from rendering code.

## Configuration Validation

Special care was taken to ensure invalid configuration files produce readable error messages.

---

# Final Result

The final project delivers:

- Procedurally generated mazes
- Four autonomous ghosts
- Pac-Gums and Super Pac-Gums
- Persistent highscores
- Multiple game screens
- Configuration validation
- Deployable package

while following the requirements defined in the project subject.