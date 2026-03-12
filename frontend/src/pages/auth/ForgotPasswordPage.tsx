export function ForgotPasswordPage() {
  return (
    <div className="card shadow" style={{ maxWidth: '400px', width: '100%' }}>
      <div className="card-body p-4">
        <h1 className="h3 mb-4 text-center">Forgot Password</h1>
        <p className="text-muted mb-4">
          Enter your email address and we'll send you a link to reset your password.
        </p>
        <form>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email</label>
            <input type="email" className="form-control" id="email" placeholder="you@example.com" />
          </div>
          <button type="submit" className="btn btn-primary w-100">Send Reset Link</button>
        </form>
        <div className="text-center mt-3">
          <a href="/login" className="text-decoration-none">← Back to login</a>
        </div>
      </div>
    </div>
  )
}

export function ResetPasswordPage() {
  return (
    <div className="card shadow" style={{ maxWidth: '400px', width: '100%' }}>
      <div className="card-body p-4">
        <h1 className="h3 mb-4 text-center">Reset Password</h1>
        <form>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">New Password</label>
            <input type="password" className="form-control" id="password" />
          </div>
          <div className="mb-3">
            <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
            <input type="password" className="form-control" id="confirmPassword" />
          </div>
          <button type="submit" className="btn btn-primary w-100">Reset Password</button>
        </form>
      </div>
    </div>
  )
}
