import {
  Button,
  Form,
  Modal,
} from "react-bootstrap";
import { FormEvent, ChangeEvent } from "react";

interface ModalProps {
    showModal: boolean;
    setShowModal: (show: boolean) => void;
    handleSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>;
    title: string;
    setTitle: (str: string) => void;
    setSelectedFile: (file: File | null) => void;
    isSubmitting: boolean;
}

export default function ModalWindow(props: ModalProps){
    return (
        <Modal show={props.showModal} onHide={() => props.setShowModal(false)} centered>
        <Form onSubmit={props.handleSubmit}>
          <Modal.Header closeButton>
            <Modal.Title>Добавить файл</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Название</Form.Label>
              <Form.Control
                value={props.title}
                onChange={(event: ChangeEvent<HTMLInputElement>) => props.setTitle(event.target.value)}
                placeholder="Например, Договор с подрядчиком"
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Файл</Form.Label>
              <Form.Control
                type="file"
                onChange={(event: ChangeEvent<HTMLInputElement>) =>
                  props.setSelectedFile((event.target as HTMLInputElement).files?.[0] ?? null)
                }
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="outline-secondary" onClick={() => props.setShowModal(false)}>
              Отмена
            </Button>
            <Button type="submit" variant="primary" disabled={props.isSubmitting}>
              {props.isSubmitting ? "Загрузка..." : "Сохранить"}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    )
}      