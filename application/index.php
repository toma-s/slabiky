<?php
require('php_scripts/load_options.php');
$lo = new LoadOptions();
$languages = $lo->get_languages();
$encodings = $lo->get_encodings();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>Syllabification</title>
    <link href="style/style.css" rel="stylesheet" media="all">
</head>

<script>
    function validateForm() {
        var file_name = document.forms["myform"]["file"].value;
        if (file_name === "") {
            alert("Please, choose the file.");
            return false;
        }
        var extension = file_name.split('.').pop();
        if ( extension !== "txt") {
            alert("Only txt extension is allowed.");
            return false;
        }
    }

    function handleSlovakOption() {
        var radioButton = document.getElementById("advanced_version");
        var option = document.getElementById("slovak");
        var default_option = document.getElementById("default_option");
        if (radioButton.checked == true){
            option.style.display = "block";
        } else {
            option.style.display = "none";
            option.selected = false;
            default_option.selected = true;
        }
    }
</script>

<body>

<div class="content">

    <h1>Analysis of linguistic data: Syllabification</h1>

    <nav>
        <a href="index.php" class="chosen">Select file</a>
        <a href="text_index.php">Insert text</a>
    </nav>

    <div class="form">

        <input type="hidden" name="type" value="file" form="myform">

        <div class="grid-container">

            <div class="grid-item">
                <label for="encoding">Encoding:</label>
                <div>
                	<select name="encoding" form="myform">
	                    <?php
	                    foreach ($encodings as $option => $value)
	                        if ($option == 'UTF-8')
	                            echo "<option value='$value' selected>$option</option>";
	                        else
	                            echo "<option value='$value'>$option</option>";
	                    ?>
                	</select>
                </div>
            </div>

            <div class="grid-item">
                <label for="language">Language:</label>
                <div>
                	<select id="language" name="language" form="myform">
	                    <option id="default_option" disabled selected value> -- select language -- </option>
	                    <?php
	                    foreach ($languages as $option => $value)
	                        if ($option == 'Slovak')
	                            echo "<option id='slovak' style='display:none' value='$value'>$option</option>";
	                        else
	                            echo "<option value='$value'>$option</option>";
	                    ?>
	                </select>
                </div>
            </div>

            <div class="grid-item version">

                <label for="version_border">Syllabification:</label>

                <div id="version_border">
                    <div class="version__option">
                        <input type="radio" name="version" value="basic" form="myform" onclick="handleSlovakOption()" checked>
                        <label for="version">
                            Basic
                            <span title="(vowels + sonorants, consonants)">
                           		<img src="https://img.icons8.com/material-outlined/24/000000/info.png" alt="info">
                        	</span>
                        </label>
                    </div>

                    <div class="version__option">
                        <input id="advanced_version" type="radio" name="version" value="advanced" form="myform" onclick="handleSlovakOption()">
                        <label for="version">
                            Advanced
                            <span title="(vowels + nasals, glides, liquids, obstruents)">
                        		<img src="https://img.icons8.com/material-outlined/24/000000/info.png" alt="info">
                        	</span>
                        </label>
                    </div>

                </div>
            </div>
            <div class="grid-item">
            	<label>Input file:</label>
            	<div>
            		<input type="file" name="file" form="myform">
	            	<p class="hint">Extension: .txt</p>
            	</div>
        	</div>
        </div>

        <div class="submit">
            <input type="submit" name="submit" value="Submit" form="myform">
        </div>

        <form id="myform" action="php_scripts/upload.php" method="post" enctype="multipart/form-data" onsubmit="return validateForm()"></form>

    </div>

    <footer>
        <span>&copy; Hallaballoo</span>
    </footer>

</div>

</body>
</html>
