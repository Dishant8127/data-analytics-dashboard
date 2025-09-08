// src/features/dashboard/components/KPIWidget.tsx
type KPIWidgetProps = {
  title: string;
  value: string;
};

const KPIWidget = ({ title, value }: KPIWidgetProps) => {
  return (
    <div style={{
      padding: "1rem",
      backgroundColor: "#2a2a2a",
      borderRadius: "8px",
      minWidth: "180px",
      textAlign: "center",
      boxShadow: "0 2px 10px rgba(0,0,0,0.2)"
    }}>
      <h4 style={{ margin: "0 0 0.5rem 0" }}>{title}</h4>
      <p style={{ fontSize: "1.5rem", fontWeight: "bold", margin: 0 }}>{value}</p>
    </div>
  );
};

export default KPIWidget;
