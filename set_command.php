<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    if (isset($data['url'])) {
        $command = [
            'command' => 'open_url',
            'url' => $data['url']
        ];
        file_put_contents('current_command.json', json_encode($command));
        echo json_encode(['status' => 'success']);
    }
}
?> 