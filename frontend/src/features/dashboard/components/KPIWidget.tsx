type KPIProps = {
  title: string;
  value: string | number;
};

const KPIWidget = ({ title, value }: KPIProps) => {
  return (
    <div style={{ border: "1px solid #ddd", padding: "1rem", borderRadius: "8px" }}>
      <h4>{title}</h4>
      <p style={{ fontSize: "1.5rem", fontWeight: "bold" }}>{value}</p>
    </div>
  );
};

export default KPIWidget;
