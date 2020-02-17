<?php
require('php_scripts/load_options.php');
$lo = new LoadOptions();
$languages = $lo->get_languages();
$encodings = $lo->get_encodings();
?>
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Syllabification</title>
    <link href="style/style.css" rel="stylesheet" media="all">
</head>

<script>
    function validateForm() {
        var text = document.forms["myform"]["text"].value;
        text = text.trim(text);
        if (text === "") {
            alert("Please, enter the text.");
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

    <h1>Analysis of linguistic data &mdash; Syllabification</h1>

    <nav>
        <a href="index.php">Select file </a>
        <a href="text_index.php" class="chosen">Insert text </a>
    </nav>

    <div class="form">

        <div class="properties">

            <div class="language">
                <label for="language">Language</label>
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

            <div class="version">

                <div class="version_option">
                    <label for="version">
                        Basic
                        <span title="(vowels + sonorants, consonants)">
                           <img src="https://img.icons8.com/material-outlined/24/000000/info.png" alt="info">
                        </span>
                    </label>
                    <input type="radio" name="version" value="basic" form="myform" onclick="handleSlovakOption()" checked>
                </div>

                <div class="version_option">
                    <label for="version">
                        Advanced
                        <span title="(vowels + nasals, glides, liquids, obstruents)">
                            <img src="https://img.icons8.com/material-outlined/24/000000/info.png" alt="info">
                        </span>
                    </label>
                    <input id="advanced_version" type="radio" name="version" value="advanced" form="myform" onclick="handleSlovakOption()">
                </div>

            </div>

        </div>

        <input type="hidden" name="type" value="text" form="myform">

        <textarea name="text" rows="15" maxlength="1500" placeholder="Enter text here..." form="myform"></textarea>

        <div class="submit">
            <input type="submit" name="submit" value="Submit" form="myform">
        </div>

        <form id="myform" action="php_scripts/upload.php" method="post" enctype="multipart/form-data" onsubmit="return validateForm()"></form>

    </div>

    <footer>
        <p>&copy; 2019 - <?php echo date("Y");?> Hallaballoo</p>
    </footer>

</div>

</body>
</html>
