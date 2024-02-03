# TSEC-Hacks-24 Hackathon: inHomeGen Project

## Overview
This repository documents our team's journey and the creation of the inHomeGen project during the TSEC-Hacks-24 Hackathon at Thadomal Shahani Engineering College, Mumbai. The hackathon took place from January 31, 2024, to February 1, 2024, with a focus on AI/ML.

## Problem Statement
Our challenge was to develop an Intelligent Interior Design Companion. Designing a home often requires professional expertise, which many individuals lack due to limited resources. Our goal was to create a Conversational AI platform enabling users to plan and visualize their home's interior effectively.

### Potential Features
- Natural language communication of preferences and ideas
- Style recommendations based on user preferences
- Interactive tools for design visualization
- Budget management for cost-effective decisions
- Suggestions for materials and color palettes
- Optimization based on user lifestyle and needs
- Progress tracking and easy revisions
- Bonus: Integration with design platforms, Advanced 3D Modeling, and Rendering

## Project: inHomeGen - Where Your Dream Home Comes True

### Team Members
- Shaun Pimenta (Team Leader)
- Atharva Pawar
- Manasvi Patil
- Shreya Palande

### Tech Stack
- Django with SQLite Database
- Image generator: Dreambooth
- SVM for Product recommendation
- PNG, JPG, JPEG to SVG (Vtracer)
- YOLO: Object Detection

### Features Showcase

#### Generative AI
- Users can write their desired design via prompts.

#### Track Progress
- Dashboard for tracking project progress.

#### Object Detection
- Detecting objects for personalized recommendations.

#### Easy Changes
- Effortless revisions for design changes.

#### Budgeting & Recommendations
- Estimated budget for each object with similar recommendations.

#### Voice Input
- Giving prompts over voice for a seamless experience.

#### SVG Downloads
- Users can download the SVG format of the generated image.

## Implementation Details

We used Dreambooth's stable diffuser model for image generation and a raw stable diffuser to change specific objects without altering the background style. Recommendations were provided based on detected objects, with buying links. Budgeting was implemented, allowing users to enter a budget for customized designs.

## Development Journey

We started by developing individual project components and gradually integrated them. Despite facing challenges and errors during integration, the learning curve was invaluable. We are proud of the progress made within the 24-hour hackathon timeframe.

Feel free to explore the codebase and share your thoughts! 🚀
