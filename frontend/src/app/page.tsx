"use client";

import { FormEvent, useEffect, useState } from "react";
import {
  Alert,
  Badge,
  Button,
  Col,
  Container,
  Row,
} from "react-bootstrap";
import { FileItem, AlertItem, PaginatedResponse } from "../type";
import { formatDate, formatSize } from "../util/format";
import { getLevelVariant, getProcessingVariant } from "../util/getVariant/getVariant";
import { filesPath, alertsPath, filetDownloadPath } from "../url/url";
import { ManagerFile, TableSection, ModalWindow, Pagination } from "../component";

export default function Page() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [title, setTitle] = useState<string>("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  // Пагинация
  const pageSize: number = 3;
  const [currentPageFiles, setCurrentPageFiles] = useState(1);
  const [totalPagesFiles, setTotalPagesFiles] = useState(1);
  const [totalFiles, setTotalFiles] = useState(0);
  const [currentPageAlerts, setCurrentPageAlerts] = useState(1);
  const [totalPagesAlerts, setTotalPagesAlerts] = useState(1);
  const [totalAlerts, setTotalAlerts] = useState(0);

  async function loadData(page: number = 1) {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const [filesResponse, alertsResponse] = await Promise.all([
        fetch(`${filesPath}?page=${page}&size=${pageSize}`, { cache: "no-store" }),
        fetch(`${alertsPath}?page=${page}&size=${pageSize}`, { cache: "no-store" }),
      ]);

      if (!filesResponse.ok || !alertsResponse.ok) {
        throw new Error("Не удалось загрузить данные");
      }

      const [filesData, alertsData] = await Promise.all([
        filesResponse.json() as Promise<PaginatedResponse<FileItem>>,
        alertsResponse.json() as Promise<PaginatedResponse<AlertItem>>,
      ]);
      setFiles(filesData.items);
      setTotalPagesFiles(filesData.pages);
      setTotalFiles(filesData.total);
      setCurrentPageFiles(filesData.page);
      setAlerts(alertsData.items);
      setTotalPagesAlerts(alertsData.pages);
      setTotalAlerts(alertsData.total);
      setCurrentPageAlerts(alertsData.page);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  const goToPage = (page: number, totalPages: number) => {
    if (page >= 1 && page <= totalPages) {
      loadData(page);
    }
  };

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || !selectedFile) {
      setErrorMessage("Укажите название и выберите файл");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append("title", title.trim());
    formData.append("file", selectedFile);

    try {
      const response = await fetch(filesPath, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Не удалось загрузить файл");
      }

      setShowModal(false);
      setTitle("");
      setSelectedFile(null);
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function deleteFile(fileID: string) {
    try{
      console.log(`${filesPath}/${fileID}`);
      const response = await fetch(`${filesPath}/${fileID}`, {
        method: "DELETE"
      });
      if (!response.ok) {
        throw new Error("Не удалось удалить файл");
      }
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    }
  }

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>

          <ManagerFile loadData={loadData} setShowModal={setShowModal}/>

          {errorMessage ? (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          ) : null}

          <TableSection<FileItem> 
            title="Файлы" obj={files} isLoading={isLoading} 
            thList={["Название", "Файл", "MIME", "Размер", "Статус", "Проверка", "Создан", "", ""]}
            notObjInfo="Файлы пока не загружены" cardClassName="shadow-sm border-0 mb-4"
            currentPage={currentPageFiles} totalPages={totalPagesFiles} goToPage={goToPage} total={totalFiles}
            children={
              files.map((file: FileItem) => (
                <tr key={file.id}>
                  <td>
                    <div className="fw-semibold">{file.title}</div>
                    <div className="small text-secondary">{file.id}</div>
                  </td>
                  <td>{file.original_name}</td>
                  <td>{file.mime_type}</td>
                  <td>{formatSize(file.size)}</td>
                  <td>
                    <Badge bg={getProcessingVariant(file.processing_status)}>
                      {file.processing_status}
                    </Badge>
                  </td>
                  <td>
                    <div className="d-flex flex-column gap-1">
                      <Badge bg={file.requires_attention ? "warning" : "success"}>
                        {file.scan_status ?? "pending"}
                      </Badge>
                      <span className="small text-secondary">
                        {file.scan_details ?? "Ожидает обработки"}
                      </span>
                    </div>
                  </td>
                  <td>{formatDate(file.created_at)}</td>
                  <td className="text-nowrap">
                    <Button
                      as="a"
                      href={filetDownloadPath(file.id)}
                      variant="outline-primary"
                      size="sm"
                    >
                      Скачать
                    </Button>
                  </td>
                  <td className="text-nowrap">
                    <Button
                      as="a"
                      onClick={() => deleteFile(file.id)}
                      variant="outline-primary"
                      size="sm"
                    >
                      Удалить
                    </Button>
                  </td>
                </tr>
              ))
            }
          />

          <TableSection<AlertItem> 
            title="Алерты" obj={alerts} isLoading={isLoading}
            thList={["ID", "File ID", "Уровень", "Сообщение", "Создан"]}  
            notObjInfo="Алертов пока нет" cardClassName="shadow-sm border-0"
            currentPage={currentPageAlerts} totalPages={totalPagesAlerts} goToPage={goToPage} total={totalAlerts}
            children={
              alerts.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td className="small">{item.file_id}</td>
                  <td>
                    <Badge bg={getLevelVariant(item.level)}>{item.level}</Badge>
                  </td>
                  <td>{item.message}</td>
                  <td>{formatDate(item.created_at)}</td>
                </tr>
              ))
            }
          />
          <Pagination
            currentPage={currentPageFiles}
            totalPages={totalPagesFiles}
            onPageChange={goToPage}
          />
        </Col>
      </Row>

      <ModalWindow 
        showModal={showModal} setShowModal={setShowModal} handleSubmit={handleSubmit} title={title} setTitle={setTitle} setSelectedFile={setSelectedFile}
        isSubmitting={isSubmitting}
      />
    </Container>
  );
}
