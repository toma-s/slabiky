<?php
require('php_scripts/load_options.php');
$lo = new LoadOptions();
$languages = $lo->get_languages();
$encodings = $lo->get_encodings();
?>
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>Syllabification</title>
    <link rel = "icon" href="site_logo.png" type = "image/x-icon"/>
    <link href="style/style.css" rel="stylesheet" media="all">
</head>

<script>
    function validateForm() {
        var text = document.forms["myform"]["text"].value;
        text = text.trim(text);
        if (text === "") {
            alert("Please, enter text.");
            return false;
        }
        var language = document.forms["myform"]["language"].value;
        if (language === "NONE") {
            alert("Please, select language.");
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
        <a href="index.php">Select file</a>
        <a href="text_index.php" class="chosen">Insert text</a>
    </nav>

    <div class="form">

        <div class="grid-container">

            <div class="grid-item">
                <label for="language">Language:</label>
                <div>
                    <select id="language" name="language" form="myform">
                        <option id="default_option" disabled selected value="NONE"> -- select language -- </option>
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

                <div>
                    <div class="version_option">
                        <input type="radio" name="version" value="basic" form="myform" onclick="handleSlovakOption()" checked>
                        <label for="version">
                            Basic
                            <span title="(vowels + sonorants, consonants)">
                               <img src="info_icon.png" alt="info_icon">
                            </span>
                        </label>
                    </div>

                    <div class="version_option">
                        <input id="advanced_version" type="radio" name="version" value="advanced" form="myform" onclick="handleSlovakOption()">
                        <label for="version">
                            Advanced
                            <span title="(vowels + nasals, glides, liquids, obstruents)">
                                <img src="info_icon.png" alt="info_icon">
                            </span>
                        </label>
                    </div>
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

        <p>
        <div class="brand">Last updated 22.03.2020 by Hallaballoo</div>

        <div class="gitHubLink">
            <a href="https://github.com/toma-s/slabiky" target="_blank">
                <img src="github_icon.png" alt="github_icon">
            </a>
        </div>
        </p>

    </footer>

</div>

</body>
</html>
