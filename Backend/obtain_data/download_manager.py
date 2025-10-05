import os
import time
import earthaccess
import requests
import concurrent.futures


# '2012-03-01', '2012-03-1' , (-180, 0, 180, 90)
def get_url(from_date, to_date):

    lon, lat = (-116,31)

    print('Searching for data...')
    results = earthaccess.search_data(
        short_name="M2T1NXSLV",
        version='5.12.4',
        temporal=(from_date, to_date),
        point=(lon, lat),
    )

    # Parse out URL from request, add to OPeNDAP URLs list for querying multiple granules
    od_files = []
    for item in results:
        for urls in item['umm']['RelatedUrls']:  # Iterate over RelatedUrls in each request step
            if 'OPENDAP' in urls.get('Description', '').upper():  # Check if 'OPENDAP' is in the Description
                url = urls['URL']
                # Add URL to list
                od_files.append(url)

    print('Number of files:', len(od_files))
    return od_files

# descarga un archivo granule
def download_granule(url, download_destiny, extension='csv', max_retries=3, retry_delay=5):
    print("Opening " + url)
    
    data_url = f'{url}.dap.{extension}'
    print("Downloading " + data_url)

    # Specify variables for subsetting
    required_variables = {'T2M', 
                          'QV2M',
                          'U2M', 
                          'V2M',
                          'time'}

    basename = os.path.basename(data_url)
    # Construir la ruta completa usando download_destiny
    filepath = os.path.join(download_destiny, basename)

    # Skip if file already downloaded
    if os.path.exists(filepath):
        print(f"File already exists, skipping: {basename}")
        return

    request_params = {'dap4.ce': ';'.join(required_variables)}
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(data_url, params=request_params, headers={'Accept-Encoding': 'identity'}, timeout=30)
            print(response.url)
            if response.ok:
                with open(filepath, 'wb') as file_handler:
                    file_handler.write(response.content)
                print(f"Downloaded successfully: {basename}")
                return
            else:
                print(f"Request failed (attempt {attempt}): {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Download error on attempt {attempt} for {basename}: {e}")
        
        if attempt < max_retries:
            time.sleep(retry_delay)

    print(f"Failed to download after {max_retries} attempts: {basename}")


# descarga los archivos de forma asincrona los datos desde una fecha a otra
def download_data_async(download_destiny, from_date, to_date):
    od_files = get_url(from_date, to_date)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(download_granule, od_files, download_destiny)


if __name__ == "__main__":
    download_destiny = './obtain_data/.M2T1NXSLV_files'
    from_date = '2012-03-01'
    to_date = '2012-03-01'

    if not os.path.exists(download_destiny):
        os.makedirs(download_destiny)
    download_data_async(download_destiny, from_date, to_date)
