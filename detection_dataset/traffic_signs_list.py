def get_traffic_signs():
    filename='traffic_signs.txt'
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip()]
        
    except FileNotFoundError:
        print(f'File {filename} not found')
        return []