
import PropTypes from "prop-types";

function Textarea({
  label,
  value,
  onChange,
  required = false,
  placeholder,
  rows = 4,
}) {
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
  );
}

Textarea.propTypes = {
  label: PropTypes.string,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  placeholder: PropTypes.string,
  rows: PropTypes.number,
};

export default Textarea;
