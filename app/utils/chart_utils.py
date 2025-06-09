def generate_chart_data(data, labels, chart_type='bar'):
    """
    Generate chart data for Chart.js
    
    Args:
        data (list): List of data points
        labels (list): List of labels
        chart_type (str): Type of chart (bar, line, pie, etc.)
        
    Returns:
        dict: Chart data configuration
    """
    colors = [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
    ]
    
    # Ensure we have enough colors
    while len(colors) < len(data):
        colors.extend(colors)
    
    if chart_type in ['bar', 'line']:
        return {
            'type': chart_type,
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Data',
                    'data': data,
                    'backgroundColor': colors[:len(data)],
                    'borderColor': colors[:len(data)],
                    'borderWidth': 1
                }]
            }
        }
    elif chart_type == 'pie':
        return {
            'type': 'pie',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': colors[:len(data)],
                    'borderColor': 'rgba(255, 255, 255, 1)',
                    'borderWidth': 1
                }]
            }
        }
    else:
        # Default to bar chart
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Data',
                    'data': data,
                    'backgroundColor': colors[:len(data)],
                    'borderColor': colors[:len(data)],
                    'borderWidth': 1
                }]
            }
        }
