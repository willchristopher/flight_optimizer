# Flight Ticket Price Optimization

A Python-based desktop application that finds the cheapest flight routes between cities using graph theory and the Bellman-Ford algorithm. The application features a graphical user interface for visualizing flight networks and calculating optimal routes.

## How It Works

The application models flight routes as a directed graph where:
- **Nodes** represent cities (airports identified by IATA codes)
- **Edges** represent direct flights between cities
- **Edge weights** represent flight prices in USD

The core pathfinding algorithm is **Bellman-Ford**, which efficiently computes the shortest path (cheapest route) from a starting city to a destination city. The algorithm:
1. Initializes all distances to infinity except the starting city (set to 0)
2. Relaxes all edges repeatedly to find minimum costs
3. Detects negative-weight cycles to ensure valid solutions
4. Reconstructs the optimal path from start to destination

## Tech Stack

### Core Technologies
- **Python 3.11+** - Primary programming language
- **tkinter** - GUI framework for the desktop interface
- **NetworkX** - Graph data structure and algorithms
- **Matplotlib** - Graph visualization and plotting

### External APIs
- **Amadeus API** - Fetches real-time flight prices
- **Aviation Stack API** - Retrieves live flight route information

### Additional Tools
- **PyInstaller** - Packages the application into standalone executables
- **requests** - HTTP library for API communication

## Features

### Dual Operating Modes
1. **Demo Mode**
   - Pre-loaded graph with 10 major US airports
   - Sample routes with mock pricing data
   - Instant startup without API calls
   - Perfect for testing and demonstrations

2. **Live Mode**
   - Fetches real flight data from Amadeus and Aviation Stack APIs
   - Pulls current pricing for available routes
   - Updates graph with live flight information
   - Supports 11 major airports: JFK, BOS, DCA, MIA, ORD, DTW, ATL, CLT, DFW, PHX, LAS

### Core Functionality
- **Cheapest Route Finder**
  - Select origin and destination cities from dropdown menus
  - Calculates optimal route using Bellman-Ford algorithm
  - Displays total cost and complete flight path
  - Highlights optimal route on the graph visualization

- **Interactive Graph Management**
  - Add new flights with custom prices
  - Remove existing flight routes
  - Real-time graph visualization updates
  - Visual feedback with highlighted paths

- **Graph Visualization**
  - Interactive network diagram of all flight routes
  - Color-coded nodes and edges:
    - Light blue nodes: Regular cities
    - Lime green nodes: Cities on optimal route
    - Black edges: Standard flights
    - Lime green edges: Flights on optimal route
  - Edge labels display flight prices
  - Dynamic layout using Kamada-Kawai algorithm

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Required Dependencies

Install the required Python packages:

```bash
pip install tkinter networkx matplotlib requests
```

Note: `tkinter` is typically included with Python installations on most systems.

### API Configuration

The application uses two external APIs for live mode:

1. **Amadeus API**
   - Already configured with test credentials in `amadeus_api.py`
   - For production use, register at [Amadeus for Developers](https://developers.amadeus.com/)

2. **Aviation Stack API**
   - Already configured with API key in `flight_data.py`
   - For production use, register at [Aviation Stack](https://aviationstack.com/)

## How to Run

### Method 1: Run from Source

1. Navigate to the project directory:
```bash
cd /path/to/flight_optimizer
```

2. Run the main script:
```bash
python main.py
```

3. Select your preferred mode:
   - Click **Demo Mode** for instant startup with sample data
   - Click **Live Mode** to fetch real flight information (requires internet connection)

### Method 2: Run Packaged Executable

If you've built the application using PyInstaller:

**macOS:**
```bash
open dist/main.app
```

**Linux:**
```bash
./dist/main
```

### Method 3: Build Your Own Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller main.spec
```

The executable will be created in the `dist/` directory.

## Usage Guide

### Finding the Cheapest Route

1. Launch the application and select your mode (Demo or Live)
2. Choose a **Starting City** from the first dropdown
3. Choose a **Destination City** from the second dropdown
4. Click **Find Cheapest Route**
5. View the results:
   - Total price displayed on the left panel
   - Complete route path shown (e.g., JFK → ORD → DEN → ATL)
   - Graph visualization highlights the optimal path in green

### Managing Flight Routes

**Adding a Flight:**
1. Enter the departure city IATA code (e.g., JFK)
2. Enter the arrival city IATA code (e.g., LAX)
3. Enter the price in USD (e.g., 299)
4. Click **Add Flight**
5. Graph updates automatically

**Removing a Flight:**
1. Enter the departure city IATA code
2. Enter the arrival city IATA code
3. Click **Remove Flight**
4. Graph updates automatically

**Refreshing the Graph:**
- Click **Show Graph** at any time to refresh the visualization

## Project Structure

```
flight_optimizer/
├── main.py              # Application entry point
├── gui_manager.py       # GUI implementation and event handlers
├── graph_manager.py     # Graph data structure and visualization
├── bellman_ford.py      # Bellman-Ford algorithm implementation
├── amadeus_api.py       # Amadeus API integration for flight prices
├── flight_data.py       # Aviation Stack API integration for routes
├── main.spec            # PyInstaller configuration
├── build/               # Build artifacts (generated)
└── dist/                # Packaged executables (generated)
```

### Module Descriptions

- **main.py** - Initializes and launches the GUI application
- **gui_manager.py** - Manages the tkinter interface, user interactions, and mode selection
- **graph_manager.py** - Handles graph operations, visualization with NetworkX and Matplotlib
- **bellman_ford.py** - Implements the shortest path algorithm and path reconstruction
- **amadeus_api.py** - Authenticates and fetches flight pricing data from Amadeus
- **flight_data.py** - Retrieves live flight routes from Aviation Stack API

## Algorithm Details

### Bellman-Ford Algorithm

The application uses the Bellman-Ford algorithm for pathfinding because:
- Handles weighted directed graphs efficiently
- Detects negative-weight cycles (prevents infinite cost reduction loops)
- Guarantees optimal solution for single-source shortest paths
- Time complexity: O(V × E) where V = vertices, E = edges

### Path Reconstruction

After computing shortest distances, the algorithm:
1. Uses predecessor tracking to build the path
2. Traverses backwards from destination to source
3. Reverses the path to show origin → destination
4. Validates path existence before displaying results

## Limitations

- Live mode requires active internet connection
- API rate limits may affect live data fetching
- Free tier API keys have usage restrictions
- Graph layout may overlap for very large networks
- No multi-leg optimization (doesn't consider layover times)

## Future Enhancements

Potential improvements for future versions:
- Support for date-specific flight searches
- Multi-city route optimization
- Layover time considerations
- Historical price tracking
- Export routes to PDF/CSV
- Mobile-responsive web interface
- Database caching for faster lookups

## Troubleshooting

**Issue:** Application won't start
- Ensure all dependencies are installed: `pip install tkinter networkx matplotlib requests`
- Verify Python version: `python --version` (requires 3.11+)

**Issue:** Live mode fails to load data
- Check internet connection
- Verify API keys are valid in `amadeus_api.py` and `flight_data.py`
- API services may be temporarily unavailable

**Issue:** Graph visualization is blank
- Click **Show Graph** button to refresh
- Ensure at least one flight route exists in the graph

**Issue:** "No path found" error
- Verify both cities exist in the graph
- Check if a connected path exists between the selected cities
- Try adding connecting flights manually

## License

This project is available for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests for:
- Bug fixes
- Performance improvements
- New features
- Documentation updates

---

Built with Python and optimized for finding the cheapest flight routes using graph theory.
