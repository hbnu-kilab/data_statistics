import os
import json

TEST_DATA_DIR = "data/test_set"
TRAIN_DATA_DIR = "data/train_set"


# json 파일에서 regions 부분을 가져옴
def load_regions(DATA_DIR):
    try:
        for file in os.listdir(DATA_DIR):
            if file.endswith(".json"):
                with open(os.path.join(DATA_DIR, file), "r") as f:
                    data = json.load(f)
                    image_id = next(iter(data.keys()), None)
                    regions = data[image_id]["regions"]
                    return regions
                
    except Exception as e:
        print(f"Error: {e}")


# image 당 region의 개수를 찾음
def find_region_count(DATA_DIR):
    all_regions_cnt = 0
    avg_regions_cnt_per_img = 0
    max_regions_cnt = float('-inf')
    min_regions_cnt = float('inf')
    regions_cnt_list = []
    avg_regions_cnt = 0
    
    try:
        total_images = 0
        for file in os.listdir(DATA_DIR):
            if file.endswith(".json"):
                with open(os.path.join(DATA_DIR, file), "r") as f:
                    data = json.load(f)
                    image_id = next(iter(data.keys()), None)
                    regions = data[image_id]["regions"]
                    
                    regions_cnt = len(regions)
                    regions_cnt_list.append(regions_cnt)
                    all_regions_cnt += regions_cnt

                    
                    total_images += 1
                    max_regions_cnt = max(max_regions_cnt, regions_cnt)
                    min_regions_cnt = min(min_regions_cnt, regions_cnt)
        
        avg_regions_cnt_per_img = round(sum(regions_cnt_list) / len(regions_cnt_list), 1)
        return all_regions_cnt, avg_regions_cnt_per_img, avg_regions_cnt, max_regions_cnt, min_regions_cnt
    
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0, 0, 0, 0


# region 당 caption의 개수를 찾음
def find_captions_count(DATA_DIR):
    total_captions = 0
    total_regions = 0
    max_captions_cnt_per_region = 0
    min_captions_cnt_per_region = float('inf')
    
    try:
        for file in os.listdir(DATA_DIR):
            if file.endswith(".json"):
                with open(os.path.join(DATA_DIR, file), "r") as f:
                    data = json.load(f)
                    image_id = next(iter(data.keys()), None)
                    regions = data[image_id]["regions"]
                    
                    for region in regions:
                        captions = region["captions"]
                        caption_count = len(captions)
                        total_captions += caption_count
                        total_regions += 1
                        max_captions_cnt_per_region = max(max_captions_cnt_per_region, caption_count)
                        min_captions_cnt_per_region = min(min_captions_cnt_per_region, caption_count)
        
        
        avg_captions_cnt_per_region = round(total_captions / total_regions, 1)
        
        return avg_captions_cnt_per_region, max_captions_cnt_per_region, min_captions_cnt_per_region
    
    
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0, 0
    
   
    
    
    


def main():
    DATA_DIRS = [TEST_DATA_DIR, TRAIN_DATA_DIR] 
    for data_dir in DATA_DIRS:
        all_regions_cnt, avg_regions_cnt_per_img, avg_regions_cnt_per_ins, max_regions_cnt_per_ins, min_regions_cnt_per_ins = find_region_count(data_dir)
        print(f"\n----- {data_dir} -----")
        print(f"전체 region 개수: {all_regions_cnt}")
        print(f"이미지 내 평균 region 개수: {avg_regions_cnt_per_img}")
        print(f"instance 당 region 개수 (평균): {avg_regions_cnt_per_ins}")
        print(f"Instance 당 region 개수 (max): {max_regions_cnt_per_ins}")
        print(f"Instance 당 region 개수 (min): {min_regions_cnt_per_ins}")
        
        avg_captions_cnt_per_region, max_captions_cnt_per_region, min_captions_cnt_per_region  = find_captions_count(data_dir)
        print(f"\n----- {data_dir} -----")
        print(f"avg(region의 캡션): {avg_captions_cnt_per_region}")
        print(f"max(region의 캡션): {max_captions_cnt_per_region}")
        print(f"min(region의 캡션): {min_captions_cnt_per_region}")
        
        
        
        
if __name__ == "__main__":
    main()