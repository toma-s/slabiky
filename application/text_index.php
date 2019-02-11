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
</script>

<body>

<div class="content">

    <h1>Analysis of linguistic data &mdash; Syllabification</h1>

    <nav>
        <a href="index.php">Select a file </a>
        <a href="text_index.php" class="chosen">Insert the text </a>
    </nav>

    <div class="form">

        <div class="properties">

            <div class="language">
                <label for="language">Language</label>
                <select name="language" form="myform">
                    <?php
                    foreach ($languages as $option => $value)
                        echo "<option value='$value'>$option</option>";
                    ?>
                </select>
            </div>

        </div>

        <input type="hidden" name="type" value="text" form="myform">

        <textarea name="text" rows="15" maxlength="1500" placeholder="Enter text here..."
                  form="myform"></textarea>

        <div class="submit">
            <input type="submit" name="submit" value="Submit" form="myform">
        </div>

        <form id="myform" action="php_scripts/upload.php" method="post" enctype="multipart/form-data" onsubmit="return validateForm()"></form>

    </div>

    <footer>
        <p>&copy; 2019 Hallaballoo</p>
    </footer>

</div>

</body>
</html>
