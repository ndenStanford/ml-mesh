/**
 * Autogenerated by Avro
 * 
 * DO NOT EDIT DIRECTLY
 *
 *  PL -> to be removed !!!!
 */
package com.scienceminer.nerd.kb.model.avro;  
@SuppressWarnings("all")
@org.apache.avro.specific.AvroGenerated
public class LabelSense extends org.apache.avro.specific.SpecificRecordBase implements org.apache.avro.specific.SpecificRecord {
  public static final org.apache.avro.Schema SCHEMA$ = new org.apache.avro.Schema.Parser().parse("{\"type\":\"record\",\"name\":\"LabelSense\",\"namespace\":\"com.scienceminer.nerd.kb.model.avro\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"},{\"name\":\"docCount\",\"type\":\"int\"},{\"name\":\"occCount\",\"type\":\"int\"},{\"name\":\"fromTitle\",\"type\":\"boolean\"},{\"name\":\"fromRedirect\",\"type\":\"boolean\"}]}");
  public static org.apache.avro.Schema getClassSchema() { return SCHEMA$; }
  @Deprecated public int id;
  @Deprecated public int docCount;
  @Deprecated public int occCount;
  @Deprecated public boolean fromTitle;
  @Deprecated public boolean fromRedirect;

  /**
   * Default constructor.  Note that this does not initialize fields
   * to their default values from the schema.  If that is desired then
   * one should use {@link \#newBuilder()}. 
   */
  public LabelSense() {}

  /**
   * All-args constructor.
   */
  public LabelSense(java.lang.Integer id, java.lang.Integer docCount, java.lang.Integer occCount, java.lang.Boolean fromTitle, java.lang.Boolean fromRedirect) {
    this.id = id;
    this.docCount = docCount;
    this.occCount = occCount;
    this.fromTitle = fromTitle;
    this.fromRedirect = fromRedirect;
  }

  public org.apache.avro.Schema getSchema() { return SCHEMA$; }
  // Used by DatumWriter.  Applications should not call. 
  public java.lang.Object get(int field$) {
    switch (field$) {
    case 0: return id;
    case 1: return docCount;
    case 2: return occCount;
    case 3: return fromTitle;
    case 4: return fromRedirect;
    default: throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }
  // Used by DatumReader.  Applications should not call. 
  @SuppressWarnings(value="unchecked")
  public void put(int field$, java.lang.Object value$) {
    switch (field$) {
    case 0: id = (java.lang.Integer)value$; break;
    case 1: docCount = (java.lang.Integer)value$; break;
    case 2: occCount = (java.lang.Integer)value$; break;
    case 3: fromTitle = (java.lang.Boolean)value$; break;
    case 4: fromRedirect = (java.lang.Boolean)value$; break;
    default: throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }

  /**
   * Gets the value of the 'id' field.
   */
  public java.lang.Integer getId() {
    return id;
  }

  /**
   * Sets the value of the 'id' field.
   * @param value the value to set.
   */
  public void setId(java.lang.Integer value) {
    this.id = value;
  }

  /**
   * Gets the value of the 'docCount' field.
   */
  public java.lang.Integer getDocCount() {
    return docCount;
  }

  /**
   * Sets the value of the 'docCount' field.
   * @param value the value to set.
   */
  public void setDocCount(java.lang.Integer value) {
    this.docCount = value;
  }

  /**
   * Gets the value of the 'occCount' field.
   */
  public java.lang.Integer getOccCount() {
    return occCount;
  }

  /**
   * Sets the value of the 'occCount' field.
   * @param value the value to set.
   */
  public void setOccCount(java.lang.Integer value) {
    this.occCount = value;
  }

  /**
   * Gets the value of the 'fromTitle' field.
   */
  public java.lang.Boolean getFromTitle() {
    return fromTitle;
  }

  /**
   * Sets the value of the 'fromTitle' field.
   * @param value the value to set.
   */
  public void setFromTitle(java.lang.Boolean value) {
    this.fromTitle = value;
  }

  /**
   * Gets the value of the 'fromRedirect' field.
   */
  public java.lang.Boolean getFromRedirect() {
    return fromRedirect;
  }

  /**
   * Sets the value of the 'fromRedirect' field.
   * @param value the value to set.
   */
  public void setFromRedirect(java.lang.Boolean value) {
    this.fromRedirect = value;
  }

  /** Creates a new LabelSense RecordBuilder */
  public static com.scienceminer.nerd.kb.model.avro.LabelSense.Builder newBuilder() {
    return new com.scienceminer.nerd.kb.model.avro.LabelSense.Builder();
  }
  
  /** Creates a new LabelSense RecordBuilder by copying an existing Builder */
  public static com.scienceminer.nerd.kb.model.avro.LabelSense.Builder newBuilder(com.scienceminer.nerd.kb.model.avro.LabelSense.Builder other) {
    return new com.scienceminer.nerd.kb.model.avro.LabelSense.Builder(other);
  }
  
  /** Creates a new LabelSense RecordBuilder by copying an existing LabelSense instance */
  public static com.scienceminer.nerd.kb.model.avro.LabelSense.Builder newBuilder(com.scienceminer.nerd.kb.model.avro.LabelSense other) {
    return new com.scienceminer.nerd.kb.model.avro.LabelSense.Builder(other);
  }
  
  /**
   * RecordBuilder for LabelSense instances.
   */
  public static class Builder extends org.apache.avro.specific.SpecificRecordBuilderBase<LabelSense>
    implements org.apache.avro.data.RecordBuilder<LabelSense> {

    private int id;
    private int docCount;
    private int occCount;
    private boolean fromTitle;
    private boolean fromRedirect;

    /** Creates a new Builder */
    private Builder() {
      super(com.scienceminer.nerd.kb.model.avro.LabelSense.SCHEMA$);
    }
    
    /** Creates a Builder by copying an existing Builder */
    private Builder(com.scienceminer.nerd.kb.model.avro.LabelSense.Builder other) {
      super(other);
      if (isValidValue(fields()[0], other.id)) {
        this.id = data().deepCopy(fields()[0].schema(), other.id);
        fieldSetFlags()[0] = true;
      }
      if (isValidValue(fields()[1], other.docCount)) {
        this.docCount = data().deepCopy(fields()[1].schema(), other.docCount);
        fieldSetFlags()[1] = true;
      }
      if (isValidValue(fields()[2], other.occCount)) {
        this.occCount = data().deepCopy(fields()[2].schema(), other.occCount);
        fieldSetFlags()[2] = true;
      }
      if (isValidValue(fields()[3], other.fromTitle)) {
        this.fromTitle = data().deepCopy(fields()[3].schema(), other.fromTitle);
        fieldSetFlags()[3] = true;
      }
      if (isValidValue(fields()[4], other.fromRedirect)) {
        this.fromRedirect = data().deepCopy(fields()[4].schema(), other.fromRedirect);
        fieldSetFlags()[4] = true;
      }
    }
    
    /** Creates a Builder by copying an existing LabelSense instance */
    private Builder(com.scienceminer.nerd.kb.model.avro.LabelSense other) {
            super(com.scienceminer.nerd.kb.model.avro.LabelSense.SCHEMA$);
      if (isValidValue(fields()[0], other.id)) {
        this.id = data().deepCopy(fields()[0].schema(), other.id);
        fieldSetFlags()[0] = true;
      }
      if (isValidValue(fields()[1], other.docCount)) {
        this.docCount = data().deepCopy(fields()[1].schema(), other.docCount);
        fieldSetFlags()[1] = true;
      }
      if (isValidValue(fields()[2], other.occCount)) {
        this.occCount = data().deepCopy(fields()[2].schema(), other.occCount);
        fieldSetFlags()[2] = true;
      }
      if (isValidValue(fields()[3], other.fromTitle)) {
        this.fromTitle = data().deepCopy(fields()[3].schema(), other.fromTitle);
        fieldSetFlags()[3] = true;
      }
      if (isValidValue(fields()[4], other.fromRedirect)) {
        this.fromRedirect = data().deepCopy(fields()[4].schema(), other.fromRedirect);
        fieldSetFlags()[4] = true;
      }
    }

    /** Gets the value of the 'id' field */
    public java.lang.Integer getId() {
      return id;
    }
    
    /** Sets the value of the 'id' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder setId(int value) {
      validate(fields()[0], value);
      this.id = value;
      fieldSetFlags()[0] = true;
      return this; 
    }
    
    /** Checks whether the 'id' field has been set */
    public boolean hasId() {
      return fieldSetFlags()[0];
    }
    
    /** Clears the value of the 'id' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder clearId() {
      fieldSetFlags()[0] = false;
      return this;
    }

    /** Gets the value of the 'docCount' field */
    public java.lang.Integer getDocCount() {
      return docCount;
    }
    
    /** Sets the value of the 'docCount' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder setDocCount(int value) {
      validate(fields()[1], value);
      this.docCount = value;
      fieldSetFlags()[1] = true;
      return this; 
    }
    
    /** Checks whether the 'docCount' field has been set */
    public boolean hasDocCount() {
      return fieldSetFlags()[1];
    }
    
    /** Clears the value of the 'docCount' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder clearDocCount() {
      fieldSetFlags()[1] = false;
      return this;
    }

    /** Gets the value of the 'occCount' field */
    public java.lang.Integer getOccCount() {
      return occCount;
    }
    
    /** Sets the value of the 'occCount' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder setOccCount(int value) {
      validate(fields()[2], value);
      this.occCount = value;
      fieldSetFlags()[2] = true;
      return this; 
    }
    
    /** Checks whether the 'occCount' field has been set */
    public boolean hasOccCount() {
      return fieldSetFlags()[2];
    }
    
    /** Clears the value of the 'occCount' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder clearOccCount() {
      fieldSetFlags()[2] = false;
      return this;
    }

    /** Gets the value of the 'fromTitle' field */
    public java.lang.Boolean getFromTitle() {
      return fromTitle;
    }
    
    /** Sets the value of the 'fromTitle' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder setFromTitle(boolean value) {
      validate(fields()[3], value);
      this.fromTitle = value;
      fieldSetFlags()[3] = true;
      return this; 
    }
    
    /** Checks whether the 'fromTitle' field has been set */
    public boolean hasFromTitle() {
      return fieldSetFlags()[3];
    }
    
    /** Clears the value of the 'fromTitle' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder clearFromTitle() {
      fieldSetFlags()[3] = false;
      return this;
    }

    /** Gets the value of the 'fromRedirect' field */
    public java.lang.Boolean getFromRedirect() {
      return fromRedirect;
    }
    
    /** Sets the value of the 'fromRedirect' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder setFromRedirect(boolean value) {
      validate(fields()[4], value);
      this.fromRedirect = value;
      fieldSetFlags()[4] = true;
      return this; 
    }
    
    /** Checks whether the 'fromRedirect' field has been set */
    public boolean hasFromRedirect() {
      return fieldSetFlags()[4];
    }
    
    /** Clears the value of the 'fromRedirect' field */
    public com.scienceminer.nerd.kb.model.avro.LabelSense.Builder clearFromRedirect() {
      fieldSetFlags()[4] = false;
      return this;
    }

    @Override
    public LabelSense build() {
      try {
        LabelSense record = new LabelSense();
        record.id = fieldSetFlags()[0] ? this.id : (java.lang.Integer) defaultValue(fields()[0]);
        record.docCount = fieldSetFlags()[1] ? this.docCount : (java.lang.Integer) defaultValue(fields()[1]);
        record.occCount = fieldSetFlags()[2] ? this.occCount : (java.lang.Integer) defaultValue(fields()[2]);
        record.fromTitle = fieldSetFlags()[3] ? this.fromTitle : (java.lang.Boolean) defaultValue(fields()[3]);
        record.fromRedirect = fieldSetFlags()[4] ? this.fromRedirect : (java.lang.Boolean) defaultValue(fields()[4]);
        return record;
      } catch (Exception e) {
        throw new org.apache.avro.AvroRuntimeException(e);
      }
    }
  }
}
