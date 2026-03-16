#!/bin/bash
# Download JS libraries to web/static/lib/
# Run from ~/franklins-dash/

mkdir -p web/static/lib

echo "Downloading Chart.js..."
curl -sL -o web/static/lib/chart.umd.min.js "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"

echo "Downloading SortableJS..."
curl -sL -o web/static/lib/Sortable.min.js "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.6/Sortable.min.js"

echo "Done. Files:"
ls -la web/static/lib/