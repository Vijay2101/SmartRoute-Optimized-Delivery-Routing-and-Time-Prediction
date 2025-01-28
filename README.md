
# SmartRoute-Optimized Delivery Routing & Time Prediction



SmartRoute is a logistics optimization system designed to streamline delivery operations by optimizing vehicle routes, predicting delivery times, and providing real-time operational insights. The system leverages OpenStreetMap data, machine learning models, and a dynamic dashboard for efficient fleet management.


## Features

- **Optimized Route Planning**: Uses shortest path and Traveling Salesman Problem (TSP) algorithms to determine the best delivery routes.

- **Predictive Delivery Time Estimation**: Trained machine learning model predicts delivery times based on distance, traffic, and weather conditions.

- **Dynamic Vehicle Assignment**: Orders are grouped with vehicles based on capacity, priority, and weight.

- **Interactive Dashboard**: Displays real-time route visualization, delivery metrics, and operational insights.

- **Scalable and Containerized**: Dockerized deployment with FastAPI backend and React frontend.


## Installation & Setup

Steps to Run

- Clone the repository
```bash
  git clone https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction.git
  cd SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction
```

- Start the services using Docker Compose
```bash
  docker-compose up --build
```
- Access the application
Backend API: ``` http://localhost:8000 ```

Frontend Dashboard: ``` http://localhost:3000 ```
    
## Tech Stack

- **Backend**: FastAPI, Python, OpenStreetMap (OSMnx), NetworkX
- **Frontend**: React, JavaScript, Google Maps API
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, RandomForest, Pandas, NumPy
- **Deployment**: Docker, Docker Compose


## Screenshots

![App Screenshot](https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction/blob/main/images/Screenshot%20from%202025-01-28%2011-25-18.png?raw=true)

![App Screenshot](https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction/blob/main/images/Screenshot%20from%202025-01-28%2011-25-44.png?raw=true)

![App Screenshot](https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction/blob/main/images/Screenshot%20from%202025-01-28%2011-26-06.png?raw=true)

![App Screenshot](https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction/blob/main/images/Screenshot%20from%202025-01-28%2011-26-35.png?raw=true)

![App Screenshot](https://github.com/Vijay2101/SmartRoute-Optimized-Delivery-Routing-and-Time-Prediction/blob/main/images/Screenshot%20from%202025-01-28%2011-26-43.png?raw=true)

