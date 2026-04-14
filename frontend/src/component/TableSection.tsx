import {
  Badge,
  Card,
  Spinner,
  Table,
} from "react-bootstrap";

interface TableSectionProps<T> {
    title: string;
    obj: T[];
    isLoading: boolean;
    thList: string[];
    notObjInfo: string;
    children: React.ReactNode;
    cardClassName: string;
    currentPage: number;
    totalPages: number;
    total: number;
    goToPage: (page: number, totalPages: number) => void;
}

export default function TableSection<T>(props: TableSectionProps<T>){

    return (
        <Card className={props.cardClassName}>
        <Card.Header className="bg-white border-0 pt-4 px-4">
            <div className="d-flex justify-content-between align-items-center">
            <h2 className="h5 mb-0">{props.title}</h2>
            <Badge bg="secondary">{props.total}</Badge>
            </div>
        </Card.Header>
        <Card.Body className="px-4 pb-4">
            {props.isLoading ? (
            <div className="d-flex justify-content-center py-5">
                <Spinner animation="border" />
            </div>
            ) : (
            <div className="table-responsive">
                <Table hover bordered className="align-middle mb-0">
                <thead className="table-light">
                    <tr>
                    {props.thList.map((thName: string, index: number) => (
                        <th key={index}>{thName}</th>
                    ))}
                    </tr>
                </thead>
                <tbody>
                    {props.obj.length === 0 ? (
                    <tr>
                        <td colSpan={props.thList.length} className="text-center py-4 text-secondary">
                        {props.notObjInfo}
                        </td>
                    </tr>
                    ) : (
                    props.children
                    )}
                </tbody>
                </Table>
            </div>
            )}
        </Card.Body>
        </Card>
    )
}