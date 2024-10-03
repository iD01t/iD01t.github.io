<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMEI Lookup - iUnlockMobile</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 50px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            color: #5a5aad;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #5a5aad;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #4848ad;
        }
        .result-box {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>IMEI Lookup - iUnlockMobile</h1>
        <form action="" method="POST">
            <label for="imei">Enter IMEI Number:</label>
            <input type="text" id="imei" name="imei" required placeholder="Enter IMEI number here">

            <input type="submit" value="Lookup IMEI">
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // Get the IMEI number from the form input
            $imei = htmlspecialchars($_POST['imei']);

            // API URL for IMEI Lookup (Replace with your API and key)
            $api_url = 'https://phonevalidation.abstractapi.com/v1/?api_key=YOUR_API_KEY&phone=' . $imei;

            // Initialize cURL
            $ch = curl_init();

            // Set the URL
            curl_setopt($ch, CURLOPT_URL, $api_url);

            // Set CURLOPT_RETURNTRANSFER so the content is returned as a variable.
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

            // Set CURLOPT_FOLLOWLOCATION to true to follow redirects.
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

            // Execute the request and store the result
            $data = curl_exec($ch);

            // Close the cURL handle
            curl_close($ch);

            // Display the result in a textbox
            echo "<div class='result-box'><h3>API Response:</h3><textarea rows='10' readonly>";
            echo $data;
            echo "</textarea></div>";
        }
        ?>
    </div>
</body>
</html>
