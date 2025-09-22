import './Form.css'

function Form({ onSubmit, title, children, submitText = "Salvar" }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(e)
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      {title && <h2 className="form-title">{title}</h2>}
      
      <div className="form-fields">
        {children}
      </div>
      
      <div className="form-actions">
        <button type="submit" className="form-submit">
          {submitText}
        </button>
      </div>
    </form>
  )
}

export default Form