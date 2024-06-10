# SimpleLogin Alias Deletion Tool

This Python script allows you to delete aliases from your SimpleLogin account based on specified masks. It utilizes the SimpleLogin API to retrieve and delete aliases matching the provided masks.

## Prerequisites

- Python 3.7 or higher
- `requests` library
- `python-dotenv` library

## Installation

1. Clone the repository or download the script file.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the same directory as the script and provide the following variables:
   ```
   API_KEY=your_simplelogin_api_key
   API_URL=https://app.simplelogin.io/api
   MASKS=mask1,mask2,mask3
   ```
   Replace `your_simplelogin_api_key` with your actual SimpleLogin API key, and specify the desired masks separated by commas.

## Usage

1. Open a terminal or command prompt and navigate to the directory containing the script.

2. Run the script using the following command:
   ```
   python script_name.py
   ```
   Replace `script_name.py` with the actual name of the script file.

3. The script will start the alias deletion process and display log messages indicating the progress.

4. Once the process is completed, the script will generate a `deletion_result.json` file in the same directory. This file will contain the following information:
   - `deleted_aliases`: List of aliases that were successfully deleted.
   - `total_deleted`: Total number of aliases deleted.
   - `pages_processed`: Number of pages processed during the deletion process.

## Customization

- You can modify the masks by updating the `MASKS` variable in the `.env` file. Separate multiple masks with commas.

- The script includes a small delay of 1 second between each deletion request to avoid hitting rate limits. You can adjust this delay by modifying the `time.sleep(1)` line in the `delete_aliases_by_mask` function.

## Note

- Exercise caution when using this script, as the deleted aliases cannot be recovered.

- Ensure that you have a valid SimpleLogin API key with the necessary permissions to delete aliases.

- The script assumes that the SimpleLogin API endpoints and authentication method remain the same. If there are any changes in the API, you may need to update the script accordingly.
