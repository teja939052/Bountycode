export type BountyCodeLogoProps = {
  variant?: "mark" | "wordmark" | "lockup";
  className?: string;
  title?: string;
  monochrome?: boolean;
};

const NAVY = "#17263B";
const ORANGE = "#C96F3D";

function BountyCodeMark({
  title,
  monochrome = false,
  className = "",
}: {
  title?: string;
  monochrome?: boolean;
  className?: string;
}) {
  const navy = monochrome ? "currentColor" : NAVY;
  const orange = monochrome ? "currentColor" : ORANGE;

  return (
    <svg
      viewBox="120 35 600 560"
      xmlns="http://www.w3.org/2000/svg"
      role={title ? "img" : undefined}
      aria-hidden={title ? undefined : true}
      focusable="false"
      className={`block h-full w-full ${className}`}
    >
      {title ? <title>{title}</title> : null}

      {/* Top + lower-left bands. Same navy brand color for a restrained mark. */}
      <path d="M 447.5 68.5 Q 426.0 54.0 397.5 74.0 Q 369.0 94.0 347.5 118.0 Q 326.0 142.0 310.0 170.5 Q 294.0 199.0 288.0 214.5 Q 282.0 230.0 276.5 253.0 Q 271.0 276.0 270.5 301.5 Q 270.0 327.0 267.5 327.5 Q 265.0 328.0 268.0 328.5 Q 271.0 329.0 271.0 332.0 Q 271.0 335.0 268.5 335.5 Q 266.0 336.0 266.0 341.0 Q 266.0 346.0 266.5 343.5 Q 267.0 341.0 270.0 341.5 Q 273.0 342.0 275.0 354.5 Q 277.0 367.0 290.5 396.0 Q 304.0 425.0 315.5 441.0 Q 327.0 457.0 341.5 470.0 Q 356.0 483.0 370.5 477.5 Q 385.0 472.0 401.0 462.5 Q 417.0 453.0 417.0 451.0 Q 417.0 449.0 400.0 433.0 Q 383.0 417.0 373.0 402.5 Q 363.0 388.0 353.5 365.0 Q 344.0 342.0 343.5 332.0 Q 343.0 322.0 341.0 318.0 Q 339.0 314.0 339.5 293.5 Q 340.0 273.0 341.5 272.5 Q 343.0 272.0 342.5 267.0 Q 342.0 262.0 343.5 261.5 Q 345.0 261.0 350.5 240.5 Q 356.0 220.0 370.5 196.5 Q 385.0 173.0 403.0 154.5 Q 421.0 136.0 426.5 137.0 Q 432.0 138.0 450.0 157.5 Q 468.0 177.0 478.5 195.5 Q 489.0 214.0 496.0 234.5 Q 503.0 255.0 516.5 259.5 Q 530.0 264.0 553.5 276.5 Q 577.0 289.0 572.0 260.5 Q 567.0 232.0 551.5 196.0 Q 536.0 160.0 519.5 138.0 Q 503.0 116.0 486.0 99.5 Q 469.0 83.0 447.5 68.5 Z" fill={navy} />
      <path d="M 156.0 494.0 Q 150.0 530.0 172.5 541.0 Q 195.0 552.0 214.0 557.5 Q 233.0 563.0 240.0 563.0 Q 247.0 563.0 250.0 565.0 Q 253.0 567.0 287.5 567.5 Q 322.0 568.0 322.5 566.5 Q 323.0 565.0 335.5 564.5 Q 348.0 564.0 367.5 558.5 Q 387.0 553.0 421.5 534.0 Q 456.0 515.0 480.5 493.0 Q 505.0 471.0 521.5 449.5 Q 538.0 428.0 547.0 408.5 Q 556.0 389.0 555.5 383.0 Q 555.0 377.0 543.0 367.0 Q 531.0 357.0 517.5 349.5 Q 504.0 342.0 501.5 344.0 Q 499.0 346.0 496.0 358.0 Q 493.0 370.0 480.0 392.5 Q 467.0 415.0 451.0 432.0 Q 435.0 449.0 419.0 460.5 Q 403.0 472.0 381.0 481.5 Q 359.0 491.0 327.5 497.0 Q 296.0 503.0 283.0 503.0 Q 270.0 503.0 254.5 500.5 Q 239.0 498.0 231.5 495.5 Q 224.0 493.0 226.5 478.5 Q 229.0 464.0 239.5 439.0 Q 250.0 414.0 262.0 397.5 Q 274.0 381.0 269.0 361.0 Q 264.0 341.0 263.0 326.5 Q 262.0 312.0 260.0 312.0 Q 258.0 312.0 239.0 330.5 Q 220.0 349.0 202.0 378.0 Q 184.0 407.0 173.0 432.5 Q 162.0 458.0 156.0 494.0 Z" fill={navy} />

      {/* Lower-right accent band. */}
      <path d="M 376.0 260.0 Q 351.0 266.0 349.0 288.0 Q 347.0 310.0 349.5 320.0 Q 352.0 330.0 373.5 323.5 Q 395.0 317.0 418.5 316.0 Q 442.0 315.0 458.0 318.0 Q 474.0 321.0 490.5 327.0 Q 507.0 333.0 527.0 345.5 Q 547.0 358.0 560.0 370.5 Q 573.0 383.0 585.5 401.0 Q 598.0 419.0 606.0 437.0 Q 614.0 455.0 618.0 470.0 Q 622.0 485.0 621.5 489.5 Q 621.0 494.0 609.5 497.5 Q 598.0 501.0 577.5 503.0 Q 557.0 505.0 525.5 501.0 Q 494.0 497.0 479.0 509.5 Q 464.0 522.0 449.5 531.0 Q 435.0 540.0 449.0 547.0 Q 463.0 554.0 488.0 559.5 Q 513.0 565.0 545.0 566.0 Q 577.0 567.0 578.0 565.5 Q 579.0 564.0 589.0 564.0 Q 599.0 564.0 617.0 559.5 Q 635.0 555.0 667.0 542.5 Q 699.0 530.0 699.0 522.5 Q 699.0 515.0 697.5 514.5 Q 696.0 514.0 690.5 488.0 Q 685.0 462.0 672.0 430.5 Q 659.0 399.0 644.5 376.0 Q 630.0 353.0 605.5 329.0 Q 581.0 305.0 562.0 293.0 Q 543.0 281.0 524.0 273.5 Q 505.0 266.0 485.5 261.0 Q 466.0 256.0 433.5 255.0 Q 401.0 254.0 376.0 260.0 Z" fill={orange} />
    </svg>
  );
}

function BountyCodeWordmark({
  className = "",
  monochrome = false,
}: {
  className?: string;
  monochrome?: boolean;
}) {
  return (
    <span
      className={`inline-flex whitespace-nowrap font-sans text-[2rem] font-extrabold leading-none tracking-[-0.055em] ${className}`}
      aria-label="BountyCode"
    >
      <span style={{ color: monochrome ? "currentColor" : NAVY }}>Bounty</span>
      <span style={{ color: monochrome ? "currentColor" : ORANGE }}>Code</span>
    </span>
  );
}

export function BountyCodeLogo({
  variant = "lockup",
  className = "",
  title = "BountyCode",
  monochrome = false,
}: BountyCodeLogoProps) {
  if (variant === "mark") {
    return (
      <span className={`inline-flex h-10 w-10 shrink-0 ${className}`}>
        <BountyCodeMark monochrome={monochrome} title={title} />
      </span>
    );
  }

  if (variant === "wordmark") {
    return (
      <span
        aria-label={title}
        className={`inline-flex items-baseline whitespace-nowrap font-sans text-[1.8rem] font-black leading-none tracking-[-0.055em] ${className}`}
      >
        <span style={{ color: monochrome ? "currentColor" : NAVY }}>Bounty</span>
        <span style={{ color: monochrome ? "currentColor" : ORANGE }}>Code</span>
      </span>
    );
  }

  return (
    <span
      aria-label={title}
      className={`inline-flex items-center gap-3 ${className}`}
    >
      {/* Title withheld: the wrapper's aria-label already names the lockup, so
          a titled <img role> in here would announce "BountyCode" twice. */}
      <span className="h-11 w-11 shrink-0">
        <BountyCodeMark monochrome={monochrome} />
      </span>

      <span className="inline-flex items-baseline whitespace-nowrap font-sans text-[1.8rem] font-black leading-none tracking-[-0.055em]">
        <span style={{ color: monochrome ? "currentColor" : NAVY }}>Bounty</span>
        <span style={{ color: monochrome ? "currentColor" : ORANGE }}>Code</span>
      </span>
    </span>
  );
}

export { BountyCodeMark, BountyCodeWordmark };
export default BountyCodeLogo;
