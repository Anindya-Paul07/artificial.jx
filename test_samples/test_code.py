class DataProcessor:
    def __init__(self, data):
        self.data = data
        
    def process(self):
        # Dummy method
        results = []
        for item in self.data:
            # Bare except clause (intentional issue)
            try:
                processed = self.transform(item)
                results.append(processed)
            except:
                pass
        return results
        
    def transform(self, item):
        # Another issue: double sorting (intentional)
        sorted_item = sorted(item)
        return sorted(sorted_item)
        
# Main functionality
if __name__ == "__main__":
    # Some test data
    test_data = [1, 2, 3, 4, 5]
    avg = calculate_average(test_data)
    print(f"Average: {avg}")
    
    max_val = find_max(test_data)
    print(f"Max value: {max_val}")