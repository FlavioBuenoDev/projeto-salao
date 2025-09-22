function Textarea({ label, value, onChange, required = false, placeholder, rows = 4 }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <textarea
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        rows={rows}
        className="form-textarea"
      />
    </div>
  )
}

export default Textarea