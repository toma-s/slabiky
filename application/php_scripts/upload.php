<?php
require('my_functions.php');

class Upload
{
    private $POST;
    private $FILES;
    private $mf;
    private $allOk;
    private $SITE_ROOT;
    private $fileName;
    private $path;
    private $downloadFolderName;

    public function __construct($POST, $FILES)
    {
        $this->POST = $POST;
        $this->FILES = $FILES;
        $this->mf = new MyFunctions();
        $this->allOk = False;
        $this->SITE_ROOT = $this->get_site_root();
        $this->fileName = "";
        $this->path = "";
        $this->downloadFolderName = "";
    }

    private function get_site_root()
    {
        $SITE_ROOT = realpath(dirname(__FILE__));
        $SITE_ROOT = str_replace(basename(__DIR__), "", $SITE_ROOT);
        $SITE_ROOT = str_replace('\\', '/', $SITE_ROOT);
        return $SITE_ROOT;
    }

    public function process()
    {
        $type = $this->POST['type'];

        if ($type == 'file')
            $this->process_file_input();
        else if ($type == 'text')
            $this->process_text_input();

        if ($this->allOk)
            $this->create_files_and_download();
    }

    private function process_file_input()
    {
        $this->fileName = basename($this->FILES['file']['name']);
        $fileExtension  = pathinfo($this->fileName, PATHINFO_EXTENSION);

        if ($this->FILES['file']['name'] != "" && $fileExtension == "txt") {
            $folderName = $this->mf->getRandomName($this->fileName);
            $this->path = $this->mf->createfolder($this->SITE_ROOT."temp_files/$folderName")."/";
            $this->downloadFolderName = $this->mf->createfolder($this->path.substr($this->fileName, 0, -4));

            if(!move_uploaded_file($this->FILES['file']['tmp_name'], $this->path.$this->fileName))
                echo "There was an error uploading the file, please try again!";

            $this->allOk = True;
        }
    }

    private function process_text_input()
    {
        $remove_signs = array('-', '—', '―', '—', '―', '.', ',', ':', ';', '?', '!', '[', ']', '(', ')', '{', '}',
            '⟨', '⟩', '‹', '›', '«', '»', '“', '”', '„', '’', '‘', '‚');

        $textarea = strip_tags($this->POST['text']);
        $textarea = str_replace($remove_signs, '', $textarea);

        if ($textarea != "") {
            $this->fileName = explode(" ", $textarea)[0].".txt";
            $folderName = $this->mf->getRandomName($this->fileName);
            $this->path = $this->mf->createfolder($this->SITE_ROOT."temp_files/$folderName")."/";
            $this->downloadFolderName = $this->mf->createfolder($this->path.substr($this->fileName, 0, -4));

            file_put_contents($this->path.$this->fileName, $textarea);
            $this->allOk = True;
        }
    }

    private function create_files_and_download()
    {
        $pythonPath = $this->mf->get_python_path();

        $key_exists = array_key_exists('encoding',$this->POST);
        if ($key_exists)
            $encoding = $this->POST['encoding'];
        else
            $encoding = 'UTF-8-sig';

        $language = $this->POST['language'];
        $language = $this->SITE_ROOT."py_scripts/configs/$language.json";

        passthru("$pythonPath ".$this->SITE_ROOT."py_scripts/init_terminate_module.py $this->fileName ".
            "$this->path $encoding $language");

        $this->mf->move_to_folder($this->path, $this->downloadFolderName, array($this->fileName, ".", ".."));
        $this->mf->zip_file($this->downloadFolderName);
        $this->mf->forceDownload($this->downloadFolderName.".zip");
        $this->mf->rmdir_recursive($this->path);
    }
}

$u = new Upload($_POST, $_FILES);
$u->process();