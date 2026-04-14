import {
  Button,
  Card,
} from "react-bootstrap";

interface ManageFileProps {
  loadData: () => void;        
  setShowModal: (show: boolean) => void;  
}

export default function ManageFile(props: ManageFileProps){

    return (
        <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
                <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                    <h1 className="h3 mb-2">Управление файлами</h1>
                    <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                    </p>
                </div>
                <div className="d-flex gap-2">
                    <Button variant="outline-secondary" onClick={() => props.loadData()}>
                    Обновить
                    </Button>
                    <Button variant="primary" onClick={() => props.setShowModal(true)}>
                    Добавить файл
                    </Button>
                </div>
                </div>
            </Card.Body>
        </Card>
    )
}