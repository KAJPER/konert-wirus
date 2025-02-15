<?php
header('Content-Type: application/json');

// Odczytaj komendę z pliku lub bazy danych
$command_file = 'current_command.json';
if (file_exists($command_file)) {
    echo file_get_contents($command_file);
    // Usuń komendę po odczytaniu
    unlink($command_file);
} else {
    echo json_encode(['command' => 'none']);
}
?> 