"use client";

import { Button } from "react-bootstrap";

export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number, totalPages: number) => void;
}

export default function Pagination(props: PaginationProps){
  if (props.totalPages <= 1) return null;

  return (
    <div className="d-flex justify-content-center gap-2 mt-4">
      <Button
        variant="outline-secondary"
        onClick={() => props.onPageChange(props.currentPage - 1, props.totalPages)}
        disabled={props.currentPage === 1}
      >
        ← Назад
      </Button>
      
      <span className="align-self-center mx-3">
        Страница {props.currentPage} из {props.totalPages}
      </span>
      
      <Button
        variant="outline-secondary"
        onClick={() => props.onPageChange(props.currentPage + 1, props.totalPages)}
        disabled={props.currentPage === props.totalPages}
      >
        Вперед →
      </Button>
    </div>
  );
};