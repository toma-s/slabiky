<?php

class MyFunctions
{
    public function __construct(){}

    public function getRandomName($filename)
    {
        $tmpfname = 'tmp' . md5($filename . time());
        return $tmpfname;
    }

    public function createFolder($folderName)
    {
        if (!mkdir($folderName, 0777, True))
            die('Failed to create folders...');
        return $folderName;
    }

    public function forceDownload($path)
    {
        $fileUrl = $path;
        header('Content-Type: application/octet-stream');
        header("Content-Transfer-Encoding: Binary");
        header("Content-disposition: attachment; filename=\"" . basename($fileUrl) . "\"");
        readfile($fileUrl);
    }

    public function rmdir_recursive($dir)
    {
        foreach (scandir($dir) as $file) {
            if ('.' === $file || '..' === $file) continue;
            if (is_dir("$dir/$file")) $this->rmdir_recursive("$dir/$file");
            else unlink("$dir/$file");
        }
        rmdir($dir);
    }

    public function zip_file($file)
    {
        $rootPath = realpath($file);

        // Initialize archive object
        $zip = new ZipArchive();
        $zip->open($rootPath . ".zip", ZipArchive::CREATE | ZipArchive::OVERWRITE);

        // Create recursive directory iterator
        /** @var SplFileInfo[] $files */
        $files = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($rootPath),
            RecursiveIteratorIterator::LEAVES_ONLY
        );

        foreach ($files as $name => $file) {
            // Skip directories (they would be added automatically)
            if (!$file->isDir()) {
                // Get real and relative path for current file
                $filePath = $file->getRealPath();
                $relativePath = substr($filePath, strlen($rootPath) + 1);

                // Add current file to archive
                $zip->addFile($filePath, $relativePath);
            }
        }
        // Zip archive will be created only after closing object
        $zip->close();
    }

    public function move_to_folder($source, $destination, $dontInclude)
    {
        $files = scandir($source);
        foreach ($files as $file) {
            if (!in_array($file, $dontInclude))
                @rename($source . $file, $destination . "/" . $file);
        }
    }

    public function get_python_path()
    {
        $pythonPath = file_get_contents('configs/python_path_origin.json');
        $pythonPath = json_decode($pythonPath, True);
        return $pythonPath['path'];
    }
}
