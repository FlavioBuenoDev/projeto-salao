function Input({ label, type = "text", value, onChange, required = false, placeholder }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <input
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        className="form-input"
      />
    </div>
  )
}

export default Input