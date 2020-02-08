<?php
require('my_functions.php');
require('test.php');

class BackendTests
{
    function __construct()
    {
        $this->run_tests();
    }

    function test_create_folder()
    {
        $folder = createFolder('test');
        $test = new Test('test_create_folder', file_exists($folder), True);
        $test->evaluate();
    }

    function test_remove_folder()
    {
        rmdir_recursive('test');
        $test = new Test('test_remove_folder', file_exists('test'), False);
        $test->evaluate();
    }

    function test_move_to_folder()
    {
        $folder1 = createFolder('test2')."/";
        $folder2 = createFolder('test3')."/";
        file_put_contents($folder1.'temp.txt', 'test');
        move_to_folder($folder1, $folder2, array());
        $test = new Test('test_move_to_folder', file_exists($folder2.'temp.txt'), True);
        $test->evaluate();
        rmdir_recursive($folder1);
        rmdir_recursive($folder2);
    }

    function test_zip_folder()
    {
        $folder = createFolder('test2');
        file_put_contents($folder.'/temp.txt', 'test');
        zip_file($folder);
        $test = new Test('test_zip_folder', file_exists($folder.'.zip'), True);
        $test->evaluate();
        rmdir_recursive($folder);
        unlink($folder.'.zip');
    }

    public function run_tests()
    {
        $this->test_create_folder();
        $this->test_remove_folder();
        $this->test_move_to_folder();
        $this->test_zip_folder();
    }
}

$t = new BackendTests();
